from django.contrib import admin

from doion.banks.models import Bank


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "display_name",
        "is_active",
        "logo",
        "brand_color_light",
        "brand_color_dark",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("code", "display_name")
    readonly_fields = ("created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj=obj))
        if obj:
            readonly.append("code")
        return readonly
