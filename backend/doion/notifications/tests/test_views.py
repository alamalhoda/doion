import pytest
from rest_framework import status
from rest_framework.test import APIClient

from doion.notifications.constants import NotificationStatus
from doion.notifications.constants import NotificationType
from doion.notifications.factories import NotificationFactory
from doion.notifications.models import Notification
from doion.users.factories import UserFactory

UNREAD_BEFORE_MARK_ALL = 2


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def notification(user):
    return NotificationFactory.create(
        user=user,
        type=NotificationType.MATCH_CREATED,
        channel="in_app",
        status=NotificationStatus.PENDING,
        title="Test Notification",
        message="Test message",
        related_object_type="cheque_listing",
        related_object_id="listing-123",
    )


@pytest.mark.django_db
class TestNotificationListEndpoint:
    def test_list_returns_user_notifications(self, user, notification):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/notifications/")

        assert response.status_code == status.HTTP_200_OK
        results = response.data.get("results", response.data)
        assert len(results) >= 1

    def test_list_filter_by_type(self, user):
        NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_CREATED,
            channel="in_app",
            status=NotificationStatus.PENDING,
            title="Match Created",
            message="Message 1",
        )
        NotificationFactory.create(
            user=user,
            type=NotificationType.LISTING_PUBLISHED,
            channel="in_app",
            status=NotificationStatus.PENDING,
            title="Listing Published",
            message="Message 2",
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/notifications/?type=match_created")

        assert response.status_code == status.HTTP_200_OK
        results = response.data.get("results", response.data)
        assert all(r["type"] == "match_created" for r in results)

    def test_list_filter_by_is_read(self, user):
        NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_CREATED,
            channel="in_app",
            status=NotificationStatus.READ,
            title="Read Notif",
            message="Read message",
        )
        NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_CREATED,
            channel="in_app",
            status=NotificationStatus.PENDING,
            title="Pending Notif",
            message="Pending message",
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/notifications/?is_read=false")

        assert response.status_code == status.HTTP_200_OK
        results = response.data.get("results", response.data)
        assert all(r["status"] != "read" for r in results)
        assert "unread_count" in response.data

    def test_list_requires_authentication(self):
        client = APIClient()
        response = client.get("/api/v1/notifications/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestNotificationMarkReadEndpoint:
    def test_mark_single_read(self, user, notification):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.patch(
            f"/api/v1/notifications/{notification.id}/",
            {"is_read": True},
        )

        assert response.status_code == status.HTTP_200_OK
        notification.refresh_from_db()
        assert notification.status == NotificationStatus.READ
        assert notification.read_at is not None

    def test_mark_read_other_user_notification_forbidden(self, user):
        other_user = UserFactory.create()
        notification = NotificationFactory.create(
            user=other_user,
            type=NotificationType.MATCH_CREATED,
            channel="in_app",
            status=NotificationStatus.PENDING,
            title="Other User Notif",
            message="Message",
        )

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.patch(
            f"/api/v1/notifications/{notification.id}/",
            {"is_read": True},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestNotificationMarkAllReadEndpoint:
    def test_mark_all_read(self, user):
        NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_CREATED,
            channel="in_app",
            status=NotificationStatus.PENDING,
            title="Notif 1",
            message="Message 1",
        )
        NotificationFactory.create(
            user=user,
            type=NotificationType.LISTING_PUBLISHED,
            channel="in_app",
            status=NotificationStatus.PENDING,
            title="Notif 2",
            message="Message 2",
        )
        NotificationFactory.create(
            user=user,
            type=NotificationType.MATCH_ACCEPTED,
            channel="in_app",
            status=NotificationStatus.READ,
            title="Notif 3 (already read)",
            message="Message 3",
        )

        unread_count = Notification.objects.filter(user=user, status=NotificationStatus.PENDING).count()
        assert unread_count == UNREAD_BEFORE_MARK_ALL

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post("/api/v1/notifications/mark-all-read/")

        assert response.status_code == status.HTTP_200_OK
        unread_count = Notification.objects.filter(user=user, status=NotificationStatus.PENDING).count()
        assert unread_count == 0


@pytest.mark.django_db
class TestNotificationPreferencesEndpoint:
    def test_get_preferences_creates_default(self, user):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get("/api/v1/notifications/preferences/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["in_app_enabled"] is True
        assert response.data["sms_enabled"] is False
        assert response.data["email_enabled"] is True

    def test_patch_preferences(self, user):
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.patch(
            "/api/v1/notifications/preferences/",
            {"sms_enabled": True},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["sms_enabled"] is True

    def test_preferences_requires_auth(self):
        client = APIClient()
        response = client.get("/api/v1/notifications/preferences/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
