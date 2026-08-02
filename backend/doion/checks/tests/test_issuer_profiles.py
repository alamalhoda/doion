"""API tests for issuer profiles."""

import pytest
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient

from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import IssuerProfile
from doion.identity.factories import ProfileFactory
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    user = UserFactory.create(password=get_random_string(12))
    ProfileFactory.create(user=user, role=user.role)
    return user


@pytest.mark.django_db
class TestIssuerProfileAPI:
    def test_create_issuer_profile(self, api_client, user):
        api_client.force_authenticate(user=user)

        response = api_client.post(
            "/api/v1/issuer-profiles/",
            {
                "national_or_company_id": "5555666677",
                "name": "New Issuer",
            },
            format="json",
        )

        assert response.status_code == 201
        assert IssuerProfile.objects.filter(national_or_company_id="5555666677").exists()

    def test_list_issuer_profiles_requires_auth(self, api_client):
        response = api_client.get("/api/v1/issuer-profiles/")
        assert response.status_code == 401

    def test_list_issuer_profiles_authenticated(self, api_client, user):
        IssuerProfileFactory.create(national_or_company_id="1111222233", name="A")
        api_client.force_authenticate(user=user)

        response = api_client.get("/api/v1/issuer-profiles/")

        assert response.status_code == 200
        results = response.data["results"] if "results" in response.data else response.data
        assert len(results) >= 1

    def test_patch_issuer_profile(self, api_client, user):
        issuer = IssuerProfileFactory.create(name="Old Name")
        api_client.force_authenticate(user=user)

        response = api_client.patch(
            f"/api/v1/issuer-profiles/{issuer.id}/",
            {"name": "Updated Name"},
            format="json",
        )

        assert response.status_code == 200
        issuer.refresh_from_db()
        assert issuer.name == "Updated Name"

    def test_delete_issuer_profile(self, api_client, user):
        issuer = IssuerProfileFactory.create()
        api_client.force_authenticate(user=user)

        response = api_client.delete(f"/api/v1/issuer-profiles/{issuer.id}/")

        assert response.status_code == 204
        assert not IssuerProfile.objects.filter(id=issuer.id).exists()
