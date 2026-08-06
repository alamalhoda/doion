from decimal import Decimal

from django.contrib.auth.models import Group
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.pricing.engine import calculate_suggested_rate
from doion.documents.models import Document


class IssuerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuerProfile
        fields = [
            "id",
            "national_or_company_id",
            "name",
            "credit_score",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "credit_score", "created_by", "created_at", "updated_at"]


class ChequeListingSerializer(serializers.ModelSerializer):
    issuer_profile = IssuerProfileSerializer(read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = ChequeListing
        fields = [
            "id",
            "owner_id",
            "issuer_profile",
            "bank_name",
            "cheque_serial_number",
            "face_amount",
            "due_date",
            "issuer_type",
            "issuer_name",
            "issuer_national_id",
            "description",
            "suggested_discount_rate",
            "risk_tier",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner_id", "status", "created_at", "updated_at"]


class ChequeListingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChequeListing
        fields = [
            "issuer",
            "bank_name",
            "cheque_serial_number",
            "face_amount",
            "due_date",
            "issuer_type",
            "issuer_name",
            "issuer_national_id",
            "description",
        ]

    def validate_face_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("face_amount must be greater than 0")
        return value

    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("due_date must be in the future")
        return value

    def validate_cheque_serial_number(self, value):
        if len(value) != 16 or not value.isdigit():
            raise serializers.ValidationError("sayad_number must be 16 digits")
        return value

    def validate(self, attrs):
        today = timezone.now().date()
        count = ChequeListing.objects.filter(owner=self.context["request"].user, created_at__date=today).count()
        if count >= 10:
            raise serializers.ValidationError(
                {"non_field_errors": ["Daily limit of 10 listings reached"]}
            )
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        issuer = validated_data["issuer"]

        days_to_due = (validated_data["due_date"] - timezone.now().date()).days
        rate, risk_tier = calculate_suggested_rate(
            face_amount=int(validated_data["face_amount"]),
            days_to_due=days_to_due,
            issuer_credit_score=issuer.credit_score,
        )

        listing = ChequeListing.objects.create(
            owner=request.user,
            suggested_discount_rate=rate,
            risk_tier=risk_tier,
            **validated_data,
        )
        return listing


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["document_type", "file", "file_size"]
        read_only_fields = ["file_size"]

    def create(self, validated_data):
        listing = self.context["listing"]
        document_type = validated_data["document_type"]
        uploaded_file = validated_data["file"]
        document = Document.objects.create(
            owner=listing.owner,
            related_object_type="cheque_listing",
            related_object_id=listing.id,
            document_type=document_type,
            file=uploaded_file,
            file_size=uploaded_file.size,
        )
        return document
