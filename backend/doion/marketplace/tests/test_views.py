from datetime import date
from datetime import timedelta

import pytest
from rest_framework.test import APIClient

from doion.banks.models import Bank
from doion.banks.seed import seed_catalog_banks
from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.users.factories import UserFactory


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
def published_listing_low_risk(db, investor, issuer):
    seed_catalog_banks()
    return ChequeListingFactory.create(
        published=True,
        owner=investor,
        issuer=issuer,
        bank=Bank.objects.get(code="mellat"),
        cheque_serial_number="1111222233334444",
        face_amount=500000000,
        due_date=date.today() + timedelta(days=60),
        issuer_type="legal",
        issuer_name="شرکت فناوری نوین",
        issuer_national_id="1234567890",
        risk_tier="low",
        suggested_discount_rate=3.5,
    )


@pytest.fixture
def published_listing_high_risk(db, investor, issuer):
    seed_catalog_banks()
    return ChequeListingFactory.create(
        published=True,
        owner=investor,
        issuer=issuer,
        bank=Bank.objects.get(code="saderat"),
        cheque_serial_number="5555666677778888",
        face_amount=200000000,
        due_date=date.today() + timedelta(days=20),
        issuer_type="natural",
        issuer_name="رضا کریمی",
        issuer_national_id="0012345678",
        high_risk=True,
    )


@pytest.fixture
def pending_listing(db, investor, issuer):
    return ChequeListingFactory.create(
        pending=True,
        owner=investor,
        issuer=issuer,
        bank_name="بانک تجارت",
        cheque_serial_number="9999000011112222",
        face_amount=300000000,
        due_date=date.today() + timedelta(days=45),
        issuer_type="legal",
        issuer_name="شرکت تجارت گستر",
        issuer_national_id="9876543210",
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

    def test_filter_by_bank_code(
        self, published_listing_low_risk, published_listing_high_risk
    ):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        response = client.get("/api/v1/marketplace/listings/", {"bank": "mellat"})
        results = response.data["results"] if "results" in response.data else response.data
        assert all(item["bank"]["code"] == "mellat" for item in results)
        ids = [item["id"] for item in results]
        assert published_listing_low_risk.id in ids
        assert published_listing_high_risk.id not in ids

    def test_filter_by_bank_name_alias(self, investor, issuer):
        seed_catalog_banks()
        listing = ChequeListingFactory.create(
            published=True,
            owner=investor,
            issuer=issuer,
            bank=Bank.objects.get(code="melli"),
            cheque_serial_number="1212121212121212",
        )
        client = APIClient()
        client.force_authenticate(user=investor)

        response = client.get("/api/v1/marketplace/listings/", {"bank_name": "ملی"})
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert listing.id in ids

    def test_nested_bank_on_list_and_latest(self, published_listing_low_risk):
        client = APIClient()
        client.force_authenticate(user=published_listing_low_risk.owner)

        list_response = client.get("/api/v1/marketplace/listings/")
        latest_response = client.get("/api/v1/marketplace/listings/latest/")

        results = (
            list_response.data["results"]
            if "results" in list_response.data
            else list_response.data
        )
        item = next(r for r in results if r["id"] == published_listing_low_risk.id)
        assert item["bank"]["code"] == "mellat"
        latest_item = next(
            r for r in latest_response.data if r["id"] == published_listing_low_risk.id
        )
        assert latest_item["bank"]["code"] == "mellat"
        assert "aliases" not in latest_item["bank"]

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


@pytest.mark.django_db
class TestMarketplaceLatestListingsEndpoint:
    def test_latest_is_public_and_returns_only_published(
        self,
        published_listing_low_risk,
        published_listing_high_risk,
        pending_listing,
    ):
        client = APIClient()

        response = client.get("/api/v1/marketplace/listings/latest/")

        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) <= 4
        ids = [item["id"] for item in response.data]
        assert published_listing_low_risk.id in ids
        assert published_listing_high_risk.id in ids
        assert pending_listing.id not in ids
