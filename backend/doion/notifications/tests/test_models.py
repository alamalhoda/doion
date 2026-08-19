import pytest

from doion.notifications.constants import NotificationChannel
from doion.notifications.constants import NotificationStatus
from doion.notifications.constants import NotificationType
from doion.notifications.factories import NotificationFactory
from doion.notifications.models import Notification
from doion.users.factories import UserFactory

EXPECTED_NOTIFICATION_COUNT = 2


@pytest.mark.django_db
class TestNotificationModel:
    def test_create_notification(self):
        user = UserFactory.create()
        notification = NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_CREATED,
            channel=NotificationChannel.IN_APP,
            status=NotificationStatus.PENDING,
            title="Test Notification",
            message="Test message content",
            related_object_type="cheque_listing",
            related_object_id="test-id-123",
        )

        assert notification.id is not None
        assert notification.type == NotificationType.MATCH_CREATED
        assert notification.status == NotificationStatus.PENDING
        assert notification.title == "Test Notification"
        assert str(notification) == f"Test Notification - {user}"

    def test_notification_default_status(self):
        user = UserFactory.create()
        notification = NotificationFactory.create(
            user=user,
            type=NotificationType.LISTING_PUBLISHED,
            channel=NotificationChannel.IN_APP,
            title="Default Status",
            message="Testing default status",
        )

        assert notification.status == NotificationStatus.PENDING

    def test_notification_indexes(self):
        user = UserFactory.create()
        NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_CREATED,
            channel=NotificationChannel.IN_APP,
            title="Notification 1",
            message="Message 1",
        )
        NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_ACCEPTED,
            channel=NotificationChannel.IN_APP,
            title="Notification 2",
            message="Message 2",
        )

        assert Notification.objects.filter(user=user).count() == EXPECTED_NOTIFICATION_COUNT

    def test_notification_with_read_at(self):
        user = UserFactory.create()
        notification = NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_ACCEPTED,
            channel=NotificationChannel.IN_APP,
            as_read=True,
            title="Read Notification",
            message="This is read",
        )

        assert notification.read_at is None  # Will be set via update
