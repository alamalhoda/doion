from django.utils.translation import gettext_lazy as _


class SMSProvider:
    STUB = "stub"
    KAVENEGAR = "kavenegar"
    MELIPAYAMAK = "melipayamak"

    CHOICES = [
        (STUB, _("Stub")),
        (KAVENEGAR, _("Kavenegar")),
        (MELIPAYAMAK, _("Melipayamak")),
    ]


class SMSStatus:
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

    CHOICES = [
        (PENDING, _("Pending")),
        (SENT, _("Sent")),
        (FAILED, _("Failed")),
    ]
