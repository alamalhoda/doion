from rest_framework import serializers

from doion.compliance.models import AuditEvent
from doion.compliance.models import FeatureFlag


class FeatureFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFlag
        fields = ["key", "description", "is_enabled", "is_system"]


class AuditEventSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)

    class Meta:
        model = AuditEvent
        fields = [
            "id",
            "actor",
            "actor_username",
            "event_type",
            "object_type",
            "object_id",
            "metadata",
            "ip_address",
            "created_at",
        ]
        read_only_fields = fields
