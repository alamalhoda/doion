from django.contrib import admin

from doion.notifications.models import Notification
from doion.notifications.models import NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "type", "channel", "status", "created_at"]
    list_filter = ["type", "channel", "status"]
    search_fields = ["title", "message", "user__username"]
    date_hierarchy = "created_at"


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ["user", "in_app_enabled", "sms_enabled", "email_enabled"]
    list_filter = ["in_app_enabled", "sms_enabled", "email_enabled"]
