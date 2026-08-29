from django.contrib import admin

from doion.identity.models import Profile
from doion.identity.models import Verification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "user_type", "is_verified", "created_at")
    list_filter = ("role", "user_type", "is_verified", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "national_id", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "full_name", "national_id")
    readonly_fields = ("created_at", "updated_at")
