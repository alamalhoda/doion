from datetime import date

from rest_framework import serializers

from doion.checks.models import ChequeListing
from doion.checks.serializers import IssuerProfileSerializer


class MarketplaceListingSerializer(serializers.ModelSerializer):
    issuer_profile = IssuerProfileSerializer(read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    days_to_due = serializers.SerializerMethodField()
    interest_count = serializers.SerializerMethodField()
    published_at = serializers.SerializerMethodField()

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
            "days_to_due",
            "interest_count",
            "published_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner_id",
            "status",
            "created_at",
            "updated_at",
            "days_to_due",
            "interest_count",
            "published_at",
        ]

    def get_days_to_due(self, obj):
        return (obj.due_date - date.today()).days

    def get_interest_count(self, obj):
        return 0

    def get_published_at(self, obj):
        if obj.status == ChequeListing.Status.PUBLISHED:
            return obj.updated_at
        return obj.created_at
