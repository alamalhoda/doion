from datetime import date
from datetime import timedelta

import pytest
from rest_framework.test import APIClient

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.users.tests.factories import UserFactory


@pytest.fixture
def investor(db):
    return UserFactory.create(role="investor")


@pytest.fixture
def issuer(db):
    return IssuerProfile.objects.create(
        national_or_company_id="1234567890",
        name="Test Issuer",
    )


@pytest.fixture
def published_listing_low_risk(db, investor, issuer):
    return ChequeListing.objects.create(
        owner=investor,
        issuer=issuer,
        bank_name="بانک ملت",
        cheque_serial_number="1111222233334444",
        face_amount=500000000,
        due_date=date.today() + timedelta(days=60),
        issuer_type="legal",
        issuer_name="شرکت فناوری نوین",
        issuer_national_id="1234567890",
        status=ChequeListing.Status.PUBLISHED,
        risk_tier="low",
        suggested_discount_rate=3.5,
    )


@pytest.fixture
def published_listing_high_risk(db, investor, issuer):
    return ChequeListing.objects.create(
        owner=investor,
        issuer=issuer,
        bank_name="بانک صادرات",
        cheque_serial_number="5555666677778888",
        face_amount=200000000,
        due_date=date.today() + timedelta(days=20),
        issuer_type="natural",
        issuer_name="رضا کریمی",
        issuer_national_id="0012345678",
        status=ChequeListing.Status.PUBLISHED,
        risk_tier="high",
        suggested_discount_rate=10.0,
    )


@pytest.fixture
def pending_listing(db, investor, issuer):
    return ChequeListing.objects.create(
        owner=investor,
        issuer=issuer,
        bank_name="بانک تجارت",
        cheque_serial_number="9999000011112222",
        face_amount=300000000,
        due_date=date.today() + timedelta(days=45),
        issuer_type="legal",
        issuer_name="شرکت تجارت گستر",
        issuer_national_id="9876543210",
        status=ChequeListing.Status.PENDING_MODERATION,
    )


@pytest.mark.django_db
class TestMarketplaceListingsEndpoint:
    def test_list_returns_only_published(self, published_listing_low_risk, pending_listing):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/")

        assert response.status_code == 200
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id in ids
        assert pending_listing.id not in ids

    def test_unauthenticated_access_denied(self, published_listing_low_risk):
        client = APIClient()

        response = client.get("/api/v1/marketplace/listings/")

        assert response.status_code == 401

    def test_days_to_due_present_and_positive(self, published_listing_low_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/")
        results = response.data["results"] if "results" in response.data else response.data
        item = next(r for r in results if r["id"] == published_listing_low_risk.id)
        assert "days_to_due" in item
        assert isinstance(item["days_to_due"], int)
        assert item["days_to_due"] > 0

    def test_interest_count_zero(self, published_listing_low_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/")
        results = response.data["results"] if "results" in response.data else response.data
        item = next(r for r in results if r["id"] == published_listing_low_risk.id)
        assert item["interest_count"] == 0

    def test_pagination_default_page_size(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/")
        assert response.status_code == 200
        assert "results" in response.data
        assert len(response.data["results"]) <= 20

    def test_filter_by_risk_tier(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"risk_tier": "low"})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id in ids
        assert published_listing_high_risk.id not in ids

    def test_filter_by_min_amount(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"min_amount": 300000000})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id in ids
        assert published_listing_high_risk.id not in ids

    def test_filter_by_max_amount(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"max_amount": 300000000})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id not in ids
        assert published_listing_high_risk.id in ids

    def test_filter_by_max_days_to_due(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"max_days_to_due": 30})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id not in ids
        assert published_listing_high_risk.id in ids

    def test_filter_by_issuer_type(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"issuer_type": "natural"})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id not in ids
        assert published_listing_high_risk.id in ids

    def test_filter_by_bank_name(self, published_listing_low_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"bank_name": "ملت"})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id in ids

    def test_ordering_by_face_amount_desc(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"ordering": "-face_amount"})
        results = response.data["results"] if "results" in response.data else response.data
        amounts = [item["face_amount"] for item in results]
        assert amounts == sorted(amounts, reverse=True)

    def test_ordering_by_due_date_asc(self, published_listing_low_risk, published_listing_high_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"ordering": "due_date"})
        results = response.data["results"] if "results" in response.data else response.data
        due_dates = [item["due_date"] for item in results]
        assert due_dates == sorted(due_dates)

    def test_search_by_bank_name(self, published_listing_low_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"search": "ملت"})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id in ids

    def test_cache_invalidation_on_status_change(self, published_listing_low_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response1 = client.get("/api/v1/marketplace/listings/")
        assert response1.status_code == 200

        published_listing_low_risk.status = ChequeListing.Status.EXPIRED
        published_listing_low_risk.save()

        response2 = client.get("/api/v1/marketplace/listings/")
        assert response2.status_code == 200
        results = response2.data["results"] if "results" in response2.data else response2.data
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id not in ids
