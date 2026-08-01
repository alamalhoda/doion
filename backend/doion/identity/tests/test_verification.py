import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from doion.identity.factories import ProfileFactory
from doion.identity.factories import VerificationFactory
from doion.identity.models import Verification
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return UserFactory.create(username="testuser")


@pytest.fixture
def test_user_with_profile(test_user):
    ProfileFactory.create(user=test_user, role=test_user.role)
    return test_user


@pytest.fixture
def authenticated_client(api_client, test_user_with_profile):
    api_client.force_authenticate(user=test_user_with_profile)
    return api_client


@pytest.fixture
def moderator_user(db):
    user = UserFactory.create(username="moduser", as_moderator=True)
    ProfileFactory.create(user=user, role=user.role)
    return user


@pytest.fixture
def moderator_client(api_client, moderator_user):
    api_client.force_authenticate(user=moderator_user)
    return api_client


@pytest.mark.django_db
class TestVerificationAPI:
    def test_create_verification(self, authenticated_client, test_user_with_profile):
        url = "/api/v1/verifications/"
        front_file = SimpleUploadedFile("front.jpg", b"fake image content", content_type="image/jpeg")
        back_file = SimpleUploadedFile("back.jpg", b"fake image content", content_type="image/jpeg")
        data = {
            "full_name": "Test User",
            "national_id": "1234567890",
            "company_name": "Test Company",
            "national_id_front": front_file,
            "national_id_back": back_file,
        }
        response = authenticated_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert Verification.objects.filter(user=test_user_with_profile).exists()

    def test_get_my_verification(self, authenticated_client, test_user_with_profile):
        VerificationFactory.create(
            user=test_user_with_profile,
            full_name="Test",
            national_id="1234567890",
        )
        url = "/api/v1/verifications/me/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "pending"

    def test_moderator_can_see_all_verifications(self, api_client, moderator_user):
        user1 = UserFactory.create(username="user1")
        user2 = UserFactory.create(username="user2", as_investor=True)
        VerificationFactory.create(user=user1, full_name="User1", national_id="1111111111")
        VerificationFactory.create(user=user2, full_name="User2", national_id="2222222222")
        api_client.force_authenticate(user=moderator_user)
        url = "/api/v1/verifications/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_regular_user_cannot_see_other_verifications(
        self, authenticated_client, test_user_with_profile,
    ):
        user2 = UserFactory.create(username="user2")
        VerificationFactory.create(user=user2, full_name="User2", national_id="2222222222")
        url = "/api/v1/verifications/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_moderator_can_approve_verification(self, api_client, moderator_user):
        holder = UserFactory.create()
        ProfileFactory.create(user=holder, role=holder.role)
        verification = VerificationFactory.create(
            user=holder,
            full_name="User1",
            national_id="1111111111",
        )
        api_client.force_authenticate(user=moderator_user)
        url = f"/api/v1/moderation/kyc/{verification.id}/decision/"
        response = api_client.post(url, {"decision": "approve"})
        assert response.status_code == status.HTTP_200_OK
        verification.refresh_from_db()
        assert verification.status == Verification.Status.APPROVED

    def test_moderator_can_reject_verification(self, api_client, moderator_user):
        holder = UserFactory.create()
        ProfileFactory.create(user=holder, role=holder.role)
        verification = VerificationFactory.create(
            user=holder,
            full_name="User1",
            national_id="1111111111",
        )
        api_client.force_authenticate(user=moderator_user)
        url = f"/api/v1/moderation/kyc/{verification.id}/decision/"
        response = api_client.post(
            url,
            {
                "decision": "reject",
                "rejection_code": "KYC_101",
                "rejection_note": "Blurry image",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        verification.refresh_from_db()
        assert verification.status == Verification.Status.REJECTED
        assert verification.rejection_code == "KYC_101"
