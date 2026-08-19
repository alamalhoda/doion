from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.checks.models import ChequeListing
from doion.core.models import TimeStampedModel
from doion.moderation.constants import RejectionCode


class ModerationDecision(TimeStampedModel):
    class Decision(models.TextChoices):
        APPROVED = "approved", _("Approved")
        REJECTED = "rejected", _("Rejected")

    listing = models.ForeignKey(
        ChequeListing,
        on_delete=models.CASCADE,
        related_name="moderation_decisions",
    )
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="moderation_decisions",
    )
    decision = models.CharField(max_length=20, choices=Decision.choices)
    rejection_code = models.CharField(  # noqa: DJ001
        max_length=20,
        choices=RejectionCode.CHOICES,
        null=True,
        blank=True,
    )
    rejection_note = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = _("Moderation Decision")
        verbose_name_plural = _("Moderation Decisions")
        indexes = [
            models.Index(fields=["listing", "-created_at"], name="moderation__listing_8f3c0e_idx"),
        ]

    def __str__(self):
        return f"{self.decision} - {self.listing}"
