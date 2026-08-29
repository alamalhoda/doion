"""Celery task tests for expire_listings (SSOT)."""

from datetime import timedelta

import pytest
from django.utils import timezone

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.integrations.tasks import expire_listings
from doion.users.factories import UserFactory


@pytest.fixture
def check_holder(db):
    return UserFactory.create()


@pytest.fixture
def issuer(db):
    return IssuerProfileFactory.create(
        national_or_company_id="1234567890",
        name="Test Issuer",
        credit_score=750,
    )


@pytest.mark.django_db
class TestExpireListingsTask:
    def test_expire_listings_changes_status(self, check_holder, issuer):
        expired_listing = ChequeListingFactory.create(
            published=True,
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="1111111111111111",
            face_amount=500000000,
            due_date=timezone.localdate() - timedelta(days=1),
            issuer_type="legal",
            issuer_name="Test Issuer",
            issuer_national_id="1234567890",
        )

        future_listing = ChequeListingFactory.create(
            published=True,
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="2222222222222222",
            face_amount=300000000,
            due_date=timezone.localdate() + timedelta(days=10),
            issuer_type="natural",
            issuer_name="Natural Issuer",
            issuer_national_id="0987654321",
        )

        result = expire_listings()

        assert result["expired_count"] == 1
        expired_listing.refresh_from_db()
        future_listing.refresh_from_db()
        assert expired_listing.status == ChequeListing.Status.EXPIRED
        assert future_listing.status == ChequeListing.Status.PUBLISHED

    def test_expire_listings_only_published(self, check_holder, issuer):
        ChequeListingFactory.create(
            matched=True,
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="3333333333333333",
            face_amount=200000000,
            due_date=timezone.localdate() - timedelta(days=1),
            issuer_type="legal",
            issuer_name="Test Issuer",
            issuer_national_id="1234567890",
        )

        result = expire_listings()

        assert result["expired_count"] == 0
