from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.core.models import TimeStampedModel
from doion.notifications.constants import NotificationChannel
from doion.notifications.constants import NotificationStatus
from doion.notifications.constants import NotificationType


class Notification(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(max_length=30, choices=NotificationType.CHOICES)
    channel = models.CharField(max_length=20, choices=NotificationChannel.CHOICES)
    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.CHOICES,
        default=NotificationStatus.PENDING,
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    related_object_id = models.CharField(max_length=255, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["user", "status", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.user}"


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
    )
    in_app_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    email_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Notification Preference")
        verbose_name_plural = _("Notification Preferences")

    def __str__(self):
        return f"Preferences for {self.user}"