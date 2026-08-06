"""API tests for cheque listings (critical create/list/my/update paths)."""

from datetime import timedelta

import pytest
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.identity.factories import ProfileFactory
from doion.identity.factories import VerificationFactory
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def check_holder(db):
    user = UserFactory.create(password=get_random_string(12))
    ProfileFactory.create(user=user, role=user.role)
    VerificationFactory.create(user=user, approved=True)
    return user


@pytest.fixture
def other_holder(db):
    user = UserFactory.create(password=get_random_string(12))
    ProfileFactory.create(user=user, role=user.role)
    VerificationFactory.create(user=user, approved=True)
    return user


@pytest.fixture
def issuer(db):
    return IssuerProfileFactory.create()


def _future_due_date(days: int = 45):
    return (timezone.now().date() + timedelta(days=days)).isoformat()


def _listing_payload(issuer, **overrides):
    payload = {
        "issuer": issuer.id,
        "bank_name": "بانک ملت",
        "cheque_serial_number": "1234567890123456",
        "face_amount": "500000000",
        "due_date": _future_due_date(),
        "issuer_type": "legal",
        "issuer_name": issuer.name,
        "issuer_national_id": issuer.national_or_company_id,
        "description": "test listing",
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
class TestChequeListingCreate:
    def test_create_listing_success_returns_201(self, api_client, check_holder, issuer):
        api_client.force_authenticate(user=check_holder)

        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer),
            format="json",
        )

        assert response.status_code == 201
        listing = ChequeListing.objects.get(owner=check_holder)
        assert listing.status == ChequeListing.Status.PENDING_MODERATION
        assert listing.suggested_discount_rate is not None
        assert listing.risk_tier in {"low", "medium", "high"}

    def test_create_listing_requires_authentication(self, api_client, issuer):
        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer),
            format="json",
        )
        assert response.status_code == 401

    def test_create_listing_rejects_non_positive_face_amount(
        self, api_client, check_holder, issuer
    ):
        api_client.force_authenticate(user=check_holder)

        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer, face_amount="0"),
            format="json",
        )

        assert response.status_code == 400

    def test_create_listing_rejects_due_date_not_in_future(
        self, api_client, check_holder, issuer
    ):
        api_client.force_authenticate(user=check_holder)

        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer, due_date=timezone.now().date().isoformat()),
            format="json",
        )

        assert response.status_code == 400

    def test_create_listing_rejects_invalid_sayad_length(
        self, api_client, check_holder, issuer
    ):
        api_client.force_authenticate(user=check_holder)

        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer, cheque_serial_number="12345"),
            format="json",
        )

        assert response.status_code == 400

    def test_create_listing_rejects_duplicate_sayad_for_issuer_bank(
        self, api_client, check_holder, issuer
    ):
        ChequeListingFactory.create(
            owner=check_holder,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="1234567890123456",
        )
        api_client.force_authenticate(user=check_holder)

        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer, cheque_serial_number="1234567890123456"),
            format="json",
        )

        assert response.status_code == 400
        assert response.data["error"]["code"] == "VALIDATION_ERROR"
        details = response.data["error"]["details"]
        detail_text = str(details)
        assert "cheque_serial_number" in detail_text or "unique" in detail_text.lower()

    def test_create_listing_rejects_when_daily_limit_reached(
        self, api_client, check_holder, issuer
    ):
        for index in range(10):
            ChequeListingFactory.create(
                owner=check_holder,
                issuer=issuer,
                cheque_serial_number=f"{2000000000000000 + index}",
            )
        api_client.force_authenticate(user=check_holder)

        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer, cheque_serial_number="3000000000000001"),
            format="json",
        )

        assert response.status_code == 400


@pytest.mark.django_db
class TestChequeListingKycGate:
    def test_create_listing_requires_approved_kyc(self, api_client, issuer, db):
        user = UserFactory.create(password=get_random_string(12))
        ProfileFactory.create(user=user, role=user.role)
        api_client.force_authenticate(user=user)

        response = api_client.post(
            "/api/v1/listings/",
            _listing_payload(issuer),
            format="json",
        )

        assert response.status_code == 403
        assert response.data["error"]["code"] == "PERMISSION_ERROR"

    def test_list_returns_only_own_listings_for_check_holder(
        self, api_client, check_holder, other_holder, issuer
    ):
        own = ChequeListingFactory.create(owner=check_holder, issuer=issuer)
        other = ChequeListingFactory.create(
            owner=other_holder,
            issuer=issuer,
            cheque_serial_number="5555666677778888",
        )
        api_client.force_authenticate(user=check_holder)

        response = api_client.get("/api/v1/listings/")

        assert response.status_code == 200
        results = response.data["results"] if "results" in response.data else response.data
        ids = [item["id"] for item in results]
        assert own.id in ids
        assert other.id not in ids

    def test_retrieve_own_listing(self, api_client, check_holder, issuer):
        listing = ChequeListingFactory.create(owner=check_holder, issuer=issuer)
        api_client.force_authenticate(user=check_holder)

        response = api_client.get(f"/api/v1/listings/{listing.id}/")

        assert response.status_code == 200
        assert response.data["id"] == listing.id

    def test_my_listings_returns_owner_listings_only(
        self, api_client, check_holder, other_holder, issuer
    ):
        own = ChequeListingFactory.create(owner=check_holder, issuer=issuer)
        ChequeListingFactory.create(
            owner=other_holder,
            issuer=issuer,
            cheque_serial_number="6666777788889999",
        )
        api_client.force_authenticate(user=check_holder)

        response = api_client.get("/api/v1/listings/my/")

        assert response.status_code == 200
        ids = [item["id"] for item in response.data]
        assert ids == [own.id]

    def test_list_requires_authentication(self, api_client):
        response = api_client.get("/api/v1/listings/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestChequeListingUpdate:
    def test_owner_can_patch_pending_listing(self, api_client, check_holder, issuer):
        listing = ChequeListingFactory.create(
            pending=True,
            owner=check_holder,
            issuer=issuer,
            description="before",
        )
        api_client.force_authenticate(user=check_holder)

        response = api_client.patch(
            f"/api/v1/listings/{listing.id}/",
            {"description": "after"},
            format="json",
        )

        assert response.status_code == 200
        listing.refresh_from_db()
        assert listing.description == "after"

    def test_patch_published_listing_returns_400(self, api_client, check_holder, issuer):
        listing = ChequeListingFactory.create(
            published=True,
            owner=check_holder,
            issuer=issuer,
        )
        api_client.force_authenticate(user=check_holder)

        response = api_client.patch(
            f"/api/v1/listings/{listing.id}/",
            {"description": "should fail"},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["error"]["code"] == "PERMISSION_ERROR"

    def test_patch_requires_authentication(self, api_client, check_holder, issuer):
        listing = ChequeListingFactory.create(owner=check_holder, issuer=issuer)

        response = api_client.patch(
            f"/api/v1/listings/{listing.id}/",
            {"description": "x"},
            format="json",
        )

        assert response.status_code == 401
