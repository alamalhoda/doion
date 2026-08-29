from rest_framework import serializers

from doion.notifications.models import Notification
from doion.notifications.models import NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "type",
            "channel",
            "status",
            "title",
            "message",
            "related_object_type",
            "related_object_id",
            "read_at",
            "sent_at",
            "created_at",
        ]
        read_only_fields = ["id", "status", "read_at", "sent_at", "created_at"]


class NotificationMarkReadSerializer(serializers.Serializer):
    is_read = serializers.BooleanField()


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ["in_app_enabled", "sms_enabled", "email_enabled"]


class NotificationListSerializer(serializers.ModelSerializer):
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "type",
            "channel",
            "status",
            "title",
            "message",
            "related_object_type",
            "related_object_id",
            "read_at",
            "sent_at",
            "created_at",
        ]

    @staticmethod
    def get_unread_count(obj):
        return 0
