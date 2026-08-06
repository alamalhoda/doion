from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.core.models import TimeStampedModel


class AuditEvent(TimeStampedModel):
    class EventType(models.TextChoices):
        LISTING_PUBLISHED = "listing_published", _("Listing Published")
        LISTING_REJECTED = "listing_rejected", _("Listing Rejected")
        KYC_APPROVED = "kyc_approved", _("KYC Approved")
        KYC_REJECTED = "kyc_rejected", _("KYC Rejected")
        FEATURE_FLAG_CHANGED = "feature_flag_changed", _("Feature Flag Changed")
        MATCH_CREATED = "match_created", _("Match Created")
        MATCH_ACCEPTED = "match_accepted", _("Match Accepted")
        MATCH_DECLINED = "match_declined", _("Match Declined")
        MATCH_CANCELLED = "match_cancelled", _("Match Cancelled")
        SETTLEMENT_CONFIRMED = "settlement_confirmed", _("Settlement Confirmed")
        LISTING_EXPIRED = "listing_expired", _("Listing Expired")

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
    )
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    object_type = models.CharField(max_length=50, blank=True)
    object_id = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.CharField(max_length=45, blank=True)

    class Meta:
        verbose_name = _("Audit Event")
        verbose_name_plural = _("Audit Events")
        indexes = [
            models.Index(fields=["event_type", "-created_at"], name="compliance_audit_event_idx"),
            models.Index(fields=["actor"], name="compliance_audit_actor_idx"),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.event_type} {self.object_type} {self.object_id}"


class FeatureFlag(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    is_enabled = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Feature Flag")
        verbose_name_plural = _("Feature Flags")
        ordering = ["key"]

    def __str__(self) -> str:
        return self.key

    @classmethod
    def is_flag_enabled(cls, key: str, default: bool = False) -> bool:
        try:
            return cls.objects.get(key=key).is_enabled
        except cls.DoesNotExist:
            return default
