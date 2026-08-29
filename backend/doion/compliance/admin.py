from django.contrib import admin

from doion.compliance.models import AuditEvent
from doion.compliance.models import FeatureFlag


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ["key", "is_enabled", "is_system", "created_at"]
    search_fields = ["key", "description"]


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ["event_type", "actor", "object_type", "object_id", "created_at"]
    list_filter = ["event_type", "actor"]
    search_fields = ["object_id", "ip_address"]
