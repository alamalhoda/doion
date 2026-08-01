import pytest

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.notifications.constants import NotificationType
from doion.notifications.models import Notification
from doion.users.factories import UserFactory


@pytest.fixture
def check_holder(db):
    return UserFactory.create()


@pytest.fixture
def investor(db):
    return UserFactory.create(as_investor=True)


@pytest.fixture
def issuer(db):
    return IssuerProfileFactory.create(
        national_or_company_id="1234567890",
        name="Test Issuer",
    )


@pytest.fixture
def moderator(db):
    return UserFactory.create(as_moderator=True)


@pytest.mark.django_db
class TestNotificationSignals:
    def test_listing_published_creates_notification(self, check_holder, issuer, moderator):
        listing = ChequeListingFactory.create(
            pending=True,
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="1234567890123456",
            face_amount=500000000,
            due_date="2026-12-31",
            issuer_type="legal",
            issuer_name="Test Issuer",
            issuer_national_id="1234567890",
        )

        # Simulate listing published signal
        from doion.moderation.signals import ChequeListingPublished
        ChequeListingPublished.send(sender=ChequeListing, listing=listing, moderator=moderator)

        notifications = Notification.objects.filter(
            user=check_holder,
            type=NotificationType.LISTING_PUBLISHED,
        )

        assert notifications.exists()
        assert notifications.first().related_object_id == str(listing.id)

    def test_listing_rejected_creates_notification(self, check_holder, issuer, moderator):
        listing = ChequeListingFactory.create(
            pending=True,
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="1234567890123456",
            face_amount=500000000,
            due_date="2026-12-31",
            issuer_type="legal",
            issuer_name="Test Issuer",
            issuer_national_id="1234567890",
        )

        from doion.moderation.signals import ListingRejected
        ListingRejected.send(
            sender=ChequeListing,
            listing=listing,
            moderator=moderator,
            rejection_code="MOD_101",
            rejection_note="Incomplete information",
        )

        notifications = Notification.objects.filter(
            user=check_holder,
            type=NotificationType.LISTING_REJECTED,
        )

        assert notifications.exists()
        assert "Incomplete information" in notifications.first().message
