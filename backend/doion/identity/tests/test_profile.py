"""API tests for identity profile / me endpoints."""

import pytest
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient

from doion.identity.factories import ProfileFactory
from doion.identity.factories import VerificationFactory
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_with_profile(db):
    user = UserFactory.create(password=get_random_string(12))
    ProfileFactory.create(user=user, role=user.role, bio="old bio")
    return user


@pytest.mark.django_db
class TestIdentityProfileAndMe:
    def test_get_profile(self, api_client, user_with_profile):
        api_client.force_authenticate(user=user_with_profile)

        response = api_client.get("/api/v1/identity/profile/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user_with_profile.username
        assert response.data["bio"] == "old bio"
        assert response.data["user_type"] == "natural"

    def test_patch_profile_cannot_change_user_type(self, api_client, user_with_profile):
        api_client.force_authenticate(user=user_with_profile)

        response = api_client.patch(
            "/api/v1/identity/profile/",
            {"user_type": "legal", "bio": "still natural"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        user_with_profile.profile.refresh_from_db()
        assert user_with_profile.profile.user_type == "natural"
        assert user_with_profile.profile.bio == "still natural"

    def test_patch_profile_updates_bio_and_name(self, api_client, user_with_profile):
        api_client.force_authenticate(user=user_with_profile)

        response = api_client.patch(
            "/api/v1/identity/profile/",
            {"bio": "new bio", "name": "Updated Name"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        user_with_profile.refresh_from_db()
        user_with_profile.profile.refresh_from_db()
        assert user_with_profile.profile.bio == "new bio"
        assert user_with_profile.name == "Updated Name"

    def test_get_identity_me(self, api_client, user_with_profile):
        api_client.force_authenticate(user=user_with_profile)

        response = api_client.get("/api/v1/identity/me/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == user_with_profile.username
        assert response.data["role"] == user_with_profile.role
        assert response.data["user_type"] == "natural"

    def test_patch_identity_me_updates_phone(self, api_client, user_with_profile):
        api_client.force_authenticate(user=user_with_profile)

        response = api_client.patch(
            "/api/v1/identity/me/",
            {"phone": "09120001122", "name": "Me Name"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        user_with_profile.refresh_from_db()
        assert user_with_profile.phone == "09120001122"
        assert user_with_profile.name == "Me Name"

    def test_profile_requires_authentication(self, api_client):
        response = api_client.get("/api/v1/identity/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestVerificationNegatives:
    def test_my_verification_returns_404_when_missing(self, api_client, user_with_profile):
        api_client.force_authenticate(user=user_with_profile)

        response = api_client.get("/api/v1/verifications/me/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_kyc_reject_requires_rejection_code(self, api_client):
        moderator = UserFactory.create(as_moderator=True)
        ProfileFactory.create(user=moderator, role=moderator.role)
        holder = UserFactory.create()
        ProfileFactory.create(user=holder, role=holder.role)
        verification = VerificationFactory.create(user=holder)

        api_client.force_authenticate(user=moderator)
        response = api_client.post(
            f"/api/v1/moderation/kyc/{verification.id}/decision/",
            {"decision": "reject", "rejection_note": "missing code"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_kyc_invalid_decision_returns_400(self, api_client):
        moderator = UserFactory.create(as_moderator=True)
        ProfileFactory.create(user=moderator, role=moderator.role)
        holder = UserFactory.create()
        verification = VerificationFactory.create(user=holder)

        api_client.force_authenticate(user=moderator)
        response = api_client.post(
            f"/api/v1/moderation/kyc/{verification.id}/decision/",
            {"decision": "maybe"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
