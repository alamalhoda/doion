import logging

from doion.integrations.constants import SMSProvider
from doion.integrations.constants import SMSStatus
from doion.integrations.models import SMSLog

logger = logging.getLogger(__name__)


def send_sms(phone_number: str, message: str, provider: str = SMSProvider.STUB) -> bool:
    """Send SMS via stub provider (logs only, no real cost)."""
    logger.info("SMS STUB - Would send to %s: %s", phone_number, message)

    SMSLog.objects.create(
        phone_number=phone_number,
        message=message,
        provider=provider,
        status=SMSStatus.SENT,
        response='{"status": "success", "message_id": "stub-123"}',
    )

    return True
