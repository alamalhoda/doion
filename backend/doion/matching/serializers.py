from rest_framework import serializers

from doion.banks.serializers import BankSummarySerializer
from doion.checks.models import ChequeListing
from doion.matching.constants import Status
from doion.matching.models import Match
from doion.matching.models import OffPlatformSettlement
from doion.matching.models import SettlementPort
from doion.users.api.serializers import UserSerializer


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerializer.Meta.model
        fields = ["id", "username", "name"]


class ChequeListingMinimalSerializer(serializers.ModelSerializer):
    bank = BankSummarySerializer(read_only=True)

    class Meta:
        model = ChequeListing
        fields = [
            "id",
            "bank",
            "bank_name",
            "face_amount",
            "due_date",
            "status",
            "created_at",
            "updated_at",
        ]


class MatchSerializer(serializers.ModelSerializer):
    listing = ChequeListingMinimalSerializer(read_only=True)
    investor = UserSummarySerializer(read_only=True)
    check_holder = UserSummarySerializer(read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "listing",
            "investor",
            "check_holder",
            "status",
            "settlement_type",
            "final_discount_rate",
            "terms",
            "message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MatchCreateSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField()
    message = serializers.CharField(required=False, default="", allow_blank=True)


class MatchStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Status.choices)
    final_discount_rate = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    terms = serializers.CharField(required=False, default="", allow_blank=True)


class SettlementPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettlementPort
        fields = [
            "id",
            "match",
            "port_number",
            "bank_name",
            "account_holder",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class OffPlatformSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffPlatformSettlement
        fields = [
            "id",
            "match",
            "confirmation_code",
            "confirmed_by",
            "confirmed_at",
            "settlement_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
