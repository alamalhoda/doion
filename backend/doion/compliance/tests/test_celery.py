from datetime import date, timedelta

import pytest

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.integrations.tasks import expire_listings
from doion.users.tests.factories import UserFactory


def _make_listing(owner, status, due_date):
    issuer = IssuerProfile.objects.create(
        national_or_company_id="1234567890", name="Test Issuer"
    )
    return ChequeListing.objects.create(
        owner=owner,
        issuer=issuer,
        bank_name="Test Bank",
        cheque_serial_number="SN-0001",
        face_amount=1000000,
        due_date=due_date,
        issuer_type="legal",
        issuer_name="Test Issuer",
        issuer_national_id="1234567890",
        status=status,
    )


@pytest.mark.django_db
def test_expire_listings_marks_published_past_due_as_expired():
    owner = UserFactory.create()
    listing = _make_listing(
        owner, ChequeListing.Status.PUBLISHED, date.today() - timedelta(days=1)
    )
    # a non-expired published listing should remain untouched
    future = _make_listing(
        owner, ChequeListing.Status.PUBLISHED, date.today() + timedelta(days=10)
    )

    result = expire_listings()

    listing.refresh_from_db()
    future.refresh_from_db()
    assert listing.status == ChequeListing.Status.EXPIRED
    assert future.status == ChequeListing.Status.PUBLISHED
    assert result["expired_count"] >= 1
