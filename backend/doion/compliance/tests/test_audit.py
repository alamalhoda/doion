from datetime import date, timedelta

import pytest

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.compliance.models import AuditEvent
from doion.moderation.signals import ChequeListingPublished
from doion.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_listing_published_signal_creates_audit_event():
    owner = UserFactory.create()
    issuer = IssuerProfile.objects.create(
        national_or_company_id="1234567890", name="Test Issuer"
    )
    listing = ChequeListing.objects.create(
        owner=owner,
        issuer=issuer,
        bank_name="Test Bank",
        cheque_serial_number="SN-AUDIT",
        face_amount=500000,
        due_date=date.today() + timedelta(days=5),
        issuer_type="legal",
        issuer_name="Test Issuer",
        issuer_national_id="1234567890",
        status=ChequeListing.Status.PUBLISHED,
    )
    moderator = UserFactory.create(role="moderator")

    ChequeListingPublished.send(sender=None, listing=listing, moderator=moderator)

    assert AuditEvent.objects.filter(
        event_type=AuditEvent.EventType.LISTING_PUBLISHED
    ).exists()
