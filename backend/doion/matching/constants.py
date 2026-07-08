from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    PENDING = "pending", _("Pending")
    ACCEPTED = "accepted", _("Accepted")
    DECLINED = "declined", _("Declined")
    CANCELLED = "cancelled", _("Cancelled")
    OFF_PLATFORM_CONFIRMED = "off_platform_confirmed", _("Off Platform Confirmed")
    SETTLED = "settled", _("Settled")


class SettlementType(models.TextChoices):
    OFF_PLATFORM = "off_platform", _("Off Platform")
    ESCROW = "escrow", _("Escrow")
    PRINCIPAL_LEDGER = "principal_ledger", _("Principal Ledger")