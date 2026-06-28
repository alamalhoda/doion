import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient

from doion.identity.models import Profile
from doion.identity.models import Verification
from doion.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="testpass123", role="check_holder")


@pytest.fixture
def test_user_with_profile(test_user):
    Profile.objects.get_or_create(user=test_user, defaults={"role": test_user.role})
    return test_user


@pytest.fixture
def authenticated_client(api_client, test_user_with_profile):
    api_client.force_authenticate(user=test_user_with_profile)
    return api_client


@pytest.fixture
def moderator_user(db):
    user = User.objects.create_user(
        username="moduser",
        password="testpass123",
        role="moderator",
        is_staff=True,
    )
    Profile.objects.get_or_create(user=user, defaults={"role": user.role})
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
        Verification.objects.create(
            user=test_user_with_profile,
            full_name="Test",
            national_id="1234567890",
        )
        url = "/api/v1/verifications/me/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "pending"

    def test_moderator_can_see_all_verifications(self, api_client, moderator_user):
        Profile.objects.get_or_create(user=moderator_user, defaults={"role": moderator_user.role})
        user1 = User.objects.create_user(username="user1", password="pass", role="check_holder")
        user2 = User.objects.create_user(username="user2", password="pass", role="investor")
        Verification.objects.create(user=user1, full_name="User1", national_id="1111111111")
        Verification.objects.create(user=user2, full_name="User2", national_id="2222222222")
        api_client.force_authenticate(user=moderator_user)
        url = "/api/v1/verifications/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_regular_user_cannot_see_other_verifications(
        self, authenticated_client, test_user_with_profile,
    ):
        user2 = User.objects.create_user(username="user2", password="pass", role="check_holder")
        Verification.objects.create(user=user2, full_name="User2", national_id="2222222222")
        url = "/api/v1/verifications/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0

    def test_moderator_can_approve_verification(self, api_client, moderator_user):
        Profile.objects.get_or_create(user=moderator_user, defaults={"role": moderator_user.role})
        verification = Verification.objects.create(
            user=moderator_user,
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
        Profile.objects.get_or_create(user=moderator_user, defaults={"role": moderator_user.role})
        verification = Verification.objects.create(
            user=moderator_user,
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
