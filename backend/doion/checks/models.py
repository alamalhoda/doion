from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.core.models import TimeStampedModel


class IssuerProfile(TimeStampedModel):
    national_or_company_id = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    credit_score = models.PositiveIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_issuer_profiles",
    )

    class Meta:
        verbose_name = _("Issuer Profile")
        verbose_name_plural = _("Issuer Profiles")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ChequeListing(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING_MODERATION = "pending_moderation", _("Pending Moderation")
        PUBLISHED = "published", _("Published")
        REJECTED = "rejected", _("Rejected")
        MATCHED = "matched", _("Matched")
        EXPIRED = "expired", _("Expired")
        WITHDRAWN = "withdrawn", _("Withdrawn")
        SETTLED_OFF_PLATFORM = "settled_off_platform", _("Settled Off Platform")

    class IssuerType(models.TextChoices):
        LEGAL = "legal", _("Legal")
        NATURAL = "natural", _("Natural")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cheque_listings",
    )
    issuer = models.ForeignKey(
        IssuerProfile,
        on_delete=models.PROTECT,
        related_name="cheque_listings",
    )
    bank_name = models.CharField(max_length=100)
    cheque_serial_number = models.CharField(max_length=50)
    face_amount = models.DecimalField(max_digits=15, decimal_places=0)
    due_date = models.DateField()
    issuer_type = models.CharField(max_length=10, choices=IssuerType.choices)
    issuer_name = models.CharField(max_length=255)
    issuer_national_id = models.CharField(max_length=20)
    description = models.TextField(blank=True, default="")

    suggested_discount_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    risk_tier = models.CharField(
        max_length=10,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING_MODERATION,
    )
    rejection_reason = models.TextField(blank=True, default="")
    rejection_code = models.CharField(
        max_length=20,
        choices=[
            ("MOD_101", "Incomplete information"),
            ("MOD_102", "Poor quality image"),
            ("MOD_103", "Invalid cheque"),
            ("MOD_104", "Duplicate listing"),
            ("MOD_105", "Risk too high"),
            ("MOD_106", "Other"),
        ],
        null=True,
        blank=True,
    )
    resubmit_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Cheque Listing")
        verbose_name_plural = _("Cheque Listings")
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["issuer", "bank_name", "cheque_serial_number"],
                name="unique_cheque_per_issuer_per_bank",
            )
        ]
        indexes = [
            models.Index(fields=["status", "due_date"]),
            models.Index(fields=["owner", "status"]),
        ]

    def __str__(self):
        return f"{self.bank_name} - {self.cheque_serial_number} ({self.face_amount:,})"
