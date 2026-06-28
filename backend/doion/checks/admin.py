from django.contrib import admin

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile


@admin.register(IssuerProfile)
class IssuerProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "national_or_company_id", "credit_score", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "national_or_company_id")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ChequeListing)
class ChequeListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "issuer",
        "bank_name",
        "cheque_serial_number",
        "face_amount",
        "due_date",
        "status",
        "created_at",
    )
    list_filter = ("status", "due_date", "issuer_type", "created_at")
    search_fields = ("bank_name", "cheque_serial_number", "issuer_name", "owner__username")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("owner", "issuer")
