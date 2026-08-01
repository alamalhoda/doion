from datetime import date, timedelta

import pytest

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.compliance.models import AuditEvent
from doion.moderation.signals import ChequeListingPublished
from doion.users.factories import UserFactory


@pytest.mark.django_db
def test_listing_published_signal_creates_audit_event():
    owner = UserFactory.create()
    issuer = IssuerProfileFactory.create(
        national_or_company_id="1234567890", name="Test Issuer"
    )
    listing = ChequeListingFactory.create(
        published=True,
        owner=owner,
        issuer=issuer,
        bank_name="Test Bank",
        cheque_serial_number="SN-AUDIT",
        face_amount=500000,
        due_date=date.today() + timedelta(days=5),
        issuer_type="legal",
        issuer_name="Test Issuer",
        issuer_national_id="1234567890",
    )
    moderator = UserFactory.create(as_moderator=True)

    ChequeListingPublished.send(sender=None, listing=listing, moderator=moderator)

    assert AuditEvent.objects.filter(
        event_type=AuditEvent.EventType.LISTING_PUBLISHED
    ).exists()
