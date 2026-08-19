from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.core.models import TimeStampedModel
from doion.integrations.constants import SMSProvider
from doion.integrations.constants import SMSStatus


class SMSLog(TimeStampedModel):
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    provider = models.CharField(max_length=20, choices=SMSProvider.CHOICES)
    status = models.CharField(max_length=20, choices=SMSStatus.CHOICES)
    response = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = _("SMS Log")
        verbose_name_plural = _("SMS Logs")

    def __str__(self):
        return f"SMS to {self.phone_number} - {self.status}"
