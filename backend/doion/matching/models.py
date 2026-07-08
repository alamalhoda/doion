from django.conf import settings
from django.db import models

from doion.checks.models import ChequeListing
from doion.core.models import TimeStampedModel
from doion.matching.constants import SettlementType, Status


class Match(TimeStampedModel):
    listing = models.ForeignKey(
        ChequeListing,
        on_delete=models.CASCADE,
        related_name="matches",
    )
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investor_matches",
    )
    check_holder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="holder_matches",
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PENDING,
    )
    settlement_type = models.CharField(
        max_length=20,
        choices=SettlementType.choices,
        default=SettlementType.OFF_PLATFORM,
    )
    final_discount_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    terms = models.TextField(blank=True, default="")
    message = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["check_holder", "status"]),
            models.Index(fields=["investor", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Match {self.id}: {self.listing} | {self.get_status_display()}"


class SettlementPort(TimeStampedModel):
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="settlement_port",
    )
    port_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    account_holder = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    class Meta:
        unique_together = [["match", "port_number"]]

    def __str__(self):
        return f"Port {self.port_number} for Match {self.match_id}"


class OffPlatformSettlement(TimeStampedModel):
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="off_platform_settlement",
    )
    confirmation_code = models.CharField(max_length=100)
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="settlement_confirmations",
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    settlement_notes = models.TextField(blank=True, default="")

    class Meta:
        unique_together = [["match"]]

    def __str__(self):
        return f"OffPlatformSettlement for Match {self.match_id}"
