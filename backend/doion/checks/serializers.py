from django.utils import timezone
from rest_framework import serializers

from doion.banks.models import Bank
from doion.banks.services import BANK_NAME_NOT_ACCEPTED
from doion.banks.services import UNKNOWN_OR_INACTIVE_BANK_CODE
from doion.banks.services import UnknownOrInactiveBankError
from doion.banks.services import apply_bank_to_listing
from doion.banks.services import get_active_by_code
from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.documents.models import Document
from doion.pricing.engine import calculate_suggested_rate


class CatalogBankInputMixin:
    def validate_bank(self, value: str) -> Bank:
        try:
            return get_active_by_code(value)
        except UnknownOrInactiveBankError as exc:
            raise serializers.ValidationError(UNKNOWN_OR_INACTIVE_BANK_CODE) from exc

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)
        if "bank_name" in self.initial_data:
            raise serializers.ValidationError({"bank": [BANK_NAME_NOT_ACCEPTED]})
        return attrs


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


class ChequeListingSerializer(CatalogBankInputMixin, serializers.ModelSerializer):
    issuer_profile = IssuerProfileSerializer(read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    bank = serializers.SlugField(write_only=True, required=False)

    class Meta:
        model = ChequeListing
        fields = [
            "id",
            "owner_id",
            "issuer_profile",
            "bank",
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
        read_only_fields = [
            "id",
            "owner_id",
            "bank_name",
            "status",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        bank = validated_data.pop("bank", None)
        instance = super().update(instance, validated_data)
        if bank is not None:
            apply_bank_to_listing(instance, bank)
            instance.save(update_fields=["bank", "bank_name", "updated_at"])
        return instance


class ChequeListingCreateSerializer(CatalogBankInputMixin, serializers.ModelSerializer):
    bank = serializers.SlugField(write_only=True)
    bank_name = serializers.CharField(read_only=True)

    class Meta:
        model = ChequeListing
        fields = [
            "issuer",
            "bank",
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
        attrs = super().validate(attrs)
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

        bank = validated_data.pop("bank")
        listing = ChequeListing(
            owner=request.user,
            suggested_discount_rate=rate,
            risk_tier=risk_tier,
            **validated_data,
        )
        apply_bank_to_listing(listing, bank)
        listing.save()
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
