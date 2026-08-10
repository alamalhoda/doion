"""API tests for verification / KYC natural vs legal validation."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from doion.identity.factories import ProfileFactory
from doion.identity.factories import VerificationFactory
from doion.identity.models import Profile
from doion.identity.models import Verification
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


def _id_files() -> dict:
    return {
        "national_id_front": SimpleUploadedFile(
            "front.jpg", b"fake image content", content_type="image/jpeg",
        ),
        "national_id_back": SimpleUploadedFile(
            "back.jpg", b"fake image content", content_type="image/jpeg",
        ),
    }


@pytest.fixture
def natural_user(db):
    user = UserFactory.create(username="naturaluser")
    ProfileFactory.create(user=user, role=user.role, user_type=Profile.UserType.NATURAL)
    return user


@pytest.fixture
def legal_user(db):
    user = UserFactory.create(username="legaluser")
    ProfileFactory.create(user=user, role=user.role, legal=True)
    return user


@pytest.fixture
def natural_client(api_client, natural_user):
    api_client.force_authenticate(user=natural_user)
    return api_client


@pytest.fixture
def legal_client(api_client, legal_user):
    api_client.force_authenticate(user=legal_user)
    return api_client


@pytest.fixture
def moderator_user(db):
    user = UserFactory.create(username="moduser", as_moderator=True)
    ProfileFactory.create(user=user, role=user.role)
    return user


@pytest.mark.django_db
class TestVerificationNatural:
    def test_create_natural_success(self, natural_client, natural_user):
        data = {
            "full_name": "Natural Person",
            "national_id": "1234567890",
            "company_name": "",
            **_id_files(),
        }
        response = natural_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        verification = Verification.objects.get(user=natural_user)
        assert verification.national_id == "1234567890"
        assert verification.company_name == ""
        assert response.data["user_type"] == "natural"

    def test_create_natural_rejects_non_10_digit_id(self, natural_client):
        data = {
            "full_name": "Natural Person",
            "national_id": "12345678901",
            **_id_files(),
        }
        response = natural_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["code"] == "VALIDATION_ERROR"
        assert "national_id" in response.data["error"]["details"]

    def test_create_natural_rejects_company_name(self, natural_client):
        data = {
            "full_name": "Natural Person",
            "national_id": "1234567890",
            "company_name": "Should Not Appear",
            **_id_files(),
        }
        response = natural_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["code"] == "VALIDATION_ERROR"
        assert "company_name" in response.data["error"]["details"]

    def test_create_natural_rejects_non_digit_id(self, natural_client):
        data = {
            "full_name": "Natural Person",
            "national_id": "123456789a",
            **_id_files(),
        }
        response = natural_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "national_id" in response.data["error"]["details"]


@pytest.mark.django_db
class TestVerificationLegal:
    def test_create_legal_success(self, legal_client, legal_user):
        data = {
            "full_name": "Authorized Representative",
            "national_id": "10100345678",
            "company_name": "Official Company Name",
            **_id_files(),
        }
        response = legal_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        verification = Verification.objects.get(user=legal_user)
        assert verification.national_id == "10100345678"
        assert verification.company_name == "Official Company Name"
        assert verification.full_name == "Authorized Representative"
        assert response.data["user_type"] == "legal"

    def test_create_legal_requires_company_name(self, legal_client):
        data = {
            "full_name": "Authorized Representative",
            "national_id": "10100345678",
            "company_name": "",
            **_id_files(),
        }
        response = legal_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["code"] == "VALIDATION_ERROR"
        assert "company_name" in response.data["error"]["details"]

    def test_create_legal_rejects_10_digit_id(self, legal_client):
        data = {
            "full_name": "Authorized Representative",
            "national_id": "1234567890",
            "company_name": "Official Company Name",
            **_id_files(),
        }
        response = legal_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "national_id" in response.data["error"]["details"]

    def test_create_legal_requires_representative_name(self, legal_client):
        data = {
            "full_name": "",
            "national_id": "10100345678",
            "company_name": "Official Company Name",
            **_id_files(),
        }
        response = legal_client.post("/api/v1/verifications/", data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "full_name" in response.data["error"]["details"]


@pytest.mark.django_db
class TestVerificationAPI:
    def test_get_my_verification(self, natural_client, natural_user):
        VerificationFactory.create(
            user=natural_user,
            full_name="Test",
            national_id="1234567890",
        )
        response = natural_client.get("/api/v1/verifications/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "pending"

    def test_moderator_can_see_all_verifications(self, api_client, moderator_user):
        user1 = UserFactory.create(username="user1")
        user2 = UserFactory.create(username="user2", as_investor=True)
        ProfileFactory.create(user=user1, role=user1.role)
        ProfileFactory.create(user=user2, role=user2.role)
        VerificationFactory.create(user=user1, full_name="User1", national_id="1111111111")
        VerificationFactory.create(user=user2, full_name="User2", national_id="2222222222")
        api_client.force_authenticate(user=moderator_user)
        response = api_client.get("/api/v1/verifications/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_regular_user_cannot_see_other_verifications(self, natural_client):
        user2 = UserFactory.create(username="user2")
        VerificationFactory.create(user=user2, full_name="User2", national_id="2222222222")
        response = natural_client.get("/api/v1/verifications/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_moderator_can_approve_verification(self, api_client, moderator_user):
        holder = UserFactory.create()
        ProfileFactory.create(user=holder, role=holder.role)
        verification = VerificationFactory.create(
            user=holder,
            full_name="Approve Me",
            national_id="1234567890",
        )
        api_client.force_authenticate(user=moderator_user)
        response = api_client.post(
            f"/api/v1/moderation/kyc/{verification.id}/decision/",
            {"decision": "approve"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        verification.refresh_from_db()
        assert verification.status == Verification.Status.APPROVED
