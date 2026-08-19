from django.contrib import admin

from doion.matching.models import Match
from doion.matching.models import OffPlatformSettlement
from doion.matching.models import SettlementPort


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "listing",
        "investor",
        "check_holder",
        "status",
        "settlement_type",
        "created_at",
    ]
    list_filter = ["status", "settlement_type", "created_at"]
    search_fields = ["listing__bank_name", "investor__username", "check_holder__username"]
    raw_id_fields = ["listing", "investor", "check_holder"]
    ordering = ["-created_at"]


@admin.register(SettlementPort)
class SettlementPortAdmin(admin.ModelAdmin):
    list_display = ["id", "match", "port_number", "bank_name", "is_verified"]
    list_filter = ["is_verified"]
    search_fields = ["port_number", "bank_name", "account_holder"]
    raw_id_fields = ["match"]


@admin.register(OffPlatformSettlement)
class OffPlatformSettlementAdmin(admin.ModelAdmin):
    list_display = ["id", "match", "confirmed_by", "confirmed_at"]
    list_filter = ["confirmed_at"]
    search_fields = ["confirmation_code", "settlement_notes"]
    raw_id_fields = ["match", "confirmed_by"]
