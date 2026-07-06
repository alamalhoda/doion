import pytest

from doion.integrations.constants import SMSProvider
from doion.integrations.constants import SMSStatus
from doion.integrations.models import SMSLog
from doion.integrations.services import send_sms


@pytest.mark.django_db
class TestSMSService:
    def test_send_sms_creates_log(self):
        result = send_sms("09123456789", "Test message")

        assert result is True
        assert SMSLog.objects.filter(phone_number="09123456789").exists()

        log = SMSLog.objects.get(phone_number="09123456789")
        assert log.message == "Test message"
        assert log.provider == SMSProvider.STUB
        assert log.status == SMSStatus.SENT

    def test_send_sms_logs_correctly(self):
        send_sms("09123456789", "Another test message", provider=SMSProvider.KAVENEGAR)

        log = SMSLog.objects.get(phone_number="09123456789")
        assert log.provider == SMSProvider.KAVENEGAR
        assert log.status == SMSStatus.SENT