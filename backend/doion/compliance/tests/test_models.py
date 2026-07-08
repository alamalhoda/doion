import pytest

from doion.compliance.models import AuditEvent
from doion.compliance.models import FeatureFlag


@pytest.mark.django_db
class TestFeatureFlag:
    def test_is_flag_enabled_returns_stored_value(self):
        FeatureFlag.objects.create(key="my_flag", is_enabled=True)
        assert FeatureFlag.is_flag_enabled("my_flag") is True

    def test_is_flag_enabled_missing_returns_default(self):
        assert FeatureFlag.is_flag_enabled("does_not_exist", default=True) is True
        assert FeatureFlag.is_flag_enabled("does_not_exist") is False

    def test_is_flag_enabled_missing_without_default_false(self):
        assert FeatureFlag.is_flag_enabled("missing") is False


@pytest.mark.django_db
class TestAuditEvent:
    def test_create_and_str(self):
        event = AuditEvent.objects.create(
            event_type=AuditEvent.EventType.LISTING_PUBLISHED,
            object_type="cheque_listing",
            object_id="123",
            ip_address="127.0.0.1",
            metadata={"foo": "bar"},
        )
        assert event.pk is not None
        assert str(event) == "listing_published cheque_listing 123"
