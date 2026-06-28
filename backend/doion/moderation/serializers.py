from rest_framework import serializers

from doion.checks.models import ChequeListing
from doion.checks.serializers import IssuerProfileSerializer
from doion.moderation.constants import RejectionCode
from doion.moderation.models import ModerationDecision


class QueueListingSerializer(serializers.ModelSerializer):
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
            "rejection_reason",
            "rejection_code",
            "resubmit_count",
            "created_at",
            "updated_at",
        ]


class ModerationDecisionSerializer(serializers.ModelSerializer):
    rejection_code_display = serializers.CharField(
        source="get_rejection_code_display", read_only=True
    )

    class Meta:
        model = ModerationDecision
        fields = [
            "id",
            "listing",
            "moderator",
            "decision",
            "rejection_code",
            "rejection_code_display",
            "rejection_note",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "rejection_code_display"]


class DecisionRequestSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=["approve", "reject"])
    rejection_code = serializers.ChoiceField(
        choices=RejectionCode.CHOICES, required=False
    )
    rejection_note = serializers.CharField(
        required=False, default="", allow_blank=True
    )
