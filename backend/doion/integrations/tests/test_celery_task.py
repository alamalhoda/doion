import pytest
from datetime import date

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.integrations.tasks import expire_listings
from doion.users.tests.factories import UserFactory


@pytest.fixture
def check_holder(db):
    return UserFactory.create(role="check_holder")


@pytest.fixture
def issuer(db):
    return IssuerProfile.objects.create(
        national_or_company_id="1234567890",
        name="Test Issuer",
        credit_score=750,
    )


@pytest.mark.django_db
class TestExpireListingsTask:
    def test_expire_listings_changes_status(self, check_holder, issuer):
        # Create expired listing
        expired_listing = ChequeListing.objects.create(
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="1111111111111111",
            face_amount=500000000,
            due_date="2020-01-01",  # Past date
            issuer_type="legal",
            issuer_name="Test Issuer",
            issuer_national_id="1234567890",
            status=ChequeListing.Status.PUBLISHED,
        )

        # Create non-expired listing
        ChequeListing.objects.create(
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="2222222222222222",
            face_amount=300000000,
            due_date="2026-12-31",  # Future date
            issuer_type="natural",
            issuer_name="Natural Issuer",
            issuer_national_id="0987654321",
            status=ChequeListing.Status.PUBLISHED,
        )

        result = expire_listings()

        assert result["expired_count"] == 1
        expired_listing.refresh_from_db()
        assert expired_listing.status == ChequeListing.Status.EXPIRED

    def test_expire_listings_only_published(self, check_holder, issuer):
        # Create matched listing (should not be expired by this task)
        ChequeListing.objects.create(
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="3333333333333333",
            face_amount=200000000,
            due_date="2020-01-01",  # Past date
            issuer_type="legal",
            issuer_name="Test Issuer",
            issuer_national_id="1234567890",
            status=ChequeListing.Status.MATCHED,
        )

        result = expire_listings()

        assert result["expired_count"] == 0