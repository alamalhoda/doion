from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.core.models import TimeStampedModel


class Profile(TimeStampedModel):
    class Role(models.TextChoices):
        CHECK_HOLDER = "check_holder", _("Check Holder")
        INVESTOR = "investor", _("Investor")
        MODERATOR = "moderator", _("Moderator")
        ADMIN = "admin", _("Admin")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CHECK_HOLDER,
    )
    bio = models.TextField(blank=True, default="")
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Verification(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        APPROVED = "approved", _("Approved")
        REJECTED = "rejected", _("Rejected")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verifications",
    )
    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=10, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.TextField(blank=True)
    rejection_code = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = _("Verification")
        verbose_name_plural = _("Verifications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.status}"
