import pytest
from rest_framework.test import APIClient

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.identity.factories import ProfileFactory
from doion.identity.factories import VerificationFactory
from doion.matching.constants import Status
from doion.matching.services import MatchingService
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def investor(db):
    user = UserFactory.create(as_investor=True)
    ProfileFactory.create(user=user, role=user.role)
    VerificationFactory.create(user=user, approved=True)
    return user


@pytest.fixture
def check_holder(db):
    user = UserFactory.create()
    ProfileFactory.create(user=user, role=user.role)
    VerificationFactory.create(user=user, approved=True)
    return user


@pytest.fixture
def issuer(db):
    return IssuerProfileFactory.create(
        national_or_company_id="1234567890",
        name="Test Issuer",
    )


def create_listing(owner, **kwargs):
    defaults = {
        "owner": owner,
        "bank_name": "Bank Melli",
        "issuer_type": "legal",
        "issuer_name": "Test Corp",
        "issuer_national_id": "987654321",
        "status": ChequeListing.Status.PUBLISHED,
    }
    if "issuer" not in kwargs:
        defaults["issuer"] = IssuerProfileFactory.create(
            national_or_company_id="1234567890",
            name="Test Issuer",
        )
    defaults.update(kwargs)
    return ChequeListingFactory.create(**defaults)


@pytest.mark.django_db
class TestMatchViewSet:
    def test_create_match_requires_investor(self, api_client, check_holder, investor, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)

        # check_holder tries to create match -> 400
        api_client.force_authenticate(user=check_holder)
        response = api_client.post(
            "/api/v1/matches/",
            {"listing_id": listing.id},
        )
        assert response.status_code == 400

        # investor successfully creates match
        api_client.force_authenticate(user=investor)
        response = api_client.post(
            "/api/v1/matches/",
            {"listing_id": listing.id},
        )
        assert response.status_code == 201
        assert response.data["status"] == Status.PENDING
        assert response.data["listing"]["id"] == listing.id

    def test_list_matches_filtered_by_role(self, api_client, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        # check_holder should see matches where they are the holder
        api_client.force_authenticate(user=check_holder)
        response = api_client.get("/api/v1/matches/")
        assert response.status_code == 200
        ids = [
            m["id"]
            for m in (
                response.data["results"] if "results" in response.data else response.data
            )
        ]
        assert match.id in ids

        # investor should see matches where they are the investor
        api_client.force_authenticate(user=investor)
        response = api_client.get("/api/v1/matches/")
        assert response.status_code == 200
        ids = [
            m["id"]
            for m in (
                response.data["results"] if "results" in response.data else response.data
            )
        ]
        assert match.id in ids

        # third party should not see the match
        third_party = UserFactory.create()
        api_client.force_authenticate(user=third_party)
        response = api_client.get("/api/v1/matches/")
        assert response.status_code == 200
        ids = [
            m["id"]
            for m in (
                response.data["results"] if "results" in response.data else response.data
            )
        ]
        assert match.id not in ids

    def test_accept_match_requires_check_holder(self, api_client, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        # investor tries to accept -> 400
        api_client.force_authenticate(user=investor)
        response = api_client.post(f"/api/v1/matches/{match.id}/accept/")
        assert response.status_code == 400

        # check_holder successfully accepts
        api_client.force_authenticate(user=check_holder)
        response = api_client.post(f"/api/v1/matches/{match.id}/accept/")
        assert response.status_code == 200
        assert response.data["status"] == Status.ACCEPTED

    def test_decline_match_requires_check_holder(self, api_client, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        # investor tries to decline -> 400
        api_client.force_authenticate(user=investor)
        response = api_client.post(
            f"/api/v1/matches/{match.id}/decline/",
            {"note": "no thanks"},
        )
        assert response.status_code == 400

        # check_holder successfully declines
        api_client.force_authenticate(user=check_holder)
        response = api_client.post(
            f"/api/v1/matches/{match.id}/decline/",
            {"note": "not interested"},
        )
        assert response.status_code == 200
        assert response.data["status"] == Status.DECLINED

    def test_cancel_match_requires_party(self, api_client, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        # third party tries to cancel -> 404 (filtered out by get_queryset)
        third_party = UserFactory.create()
        api_client.force_authenticate(user=third_party)
        response = api_client.post(f"/api/v1/matches/{match.id}/cancel/")
        assert response.status_code == 404

        # investor successfully cancels
        api_client.force_authenticate(user=investor)
        response = api_client.post(f"/api/v1/matches/{match.id}/cancel/")
        assert response.status_code == 200
        assert response.data["status"] == Status.CANCELLED

    def test_confirm_off_platform_requires_check_holder(self, api_client, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)
        accepted = MatchingService.accept_match(match.id, check_holder)

        # investor tries to confirm -> 400
        api_client.force_authenticate(user=investor)
        response = api_client.post(f"/api/v1/matches/{accepted.id}/confirm-off-platform/")
        assert response.status_code == 400

        # check_holder successfully confirms
        api_client.force_authenticate(user=check_holder)
        response = api_client.post(f"/api/v1/matches/{accepted.id}/confirm-off-platform/")
        assert response.status_code == 200
        assert response.data["status"] == Status.OFF_PLATFORM_CONFIRMED

    def test_list_requires_authentication(self, api_client):
        response = api_client.get("/api/v1/matches/")
        assert response.status_code == 401

    def test_my_matches_returns_role_filtered_results(
        self, api_client, investor, check_holder, issuer
    ):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        api_client.force_authenticate(user=investor)
        response = api_client.get("/api/v1/matches/my/")
        assert response.status_code == 200
        ids = [
            m["id"]
            for m in (
                response.data["results"] if "results" in response.data else response.data
            )
        ]
        assert match.id in ids

        api_client.force_authenticate(user=check_holder)
        response = api_client.get("/api/v1/matches/my/")
        assert response.status_code == 200
        ids = [
            m["id"]
            for m in (
                response.data["results"] if "results" in response.data else response.data
            )
        ]
        assert match.id in ids

    def test_patch_status_updates_match(self, api_client, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        api_client.force_authenticate(user=investor)
        response = api_client.patch(
            f"/api/v1/matches/{match.id}/status/",
            {"status": Status.CANCELLED, "terms": "updated terms"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["status"] == Status.CANCELLED
        assert response.data["terms"] == "updated terms"
