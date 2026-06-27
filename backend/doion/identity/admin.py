from django.contrib import admin

from doion.identity.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "is_verified", "created_at"]
    list_filter = ["role", "is_verified"]
    search_fields = ["user__username", "user__email"]
