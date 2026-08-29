"""API tests for identity registration with natural/legal user types."""

import pytest
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient

from doion.identity.models import Profile
from doion.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def check_holder_group():
    group, _ = Group.objects.get_or_create(name="CheckHolder")
    return group


@pytest.fixture
def investor_group():
    group, _ = Group.objects.get_or_create(name="Investor")
    return group


@pytest.fixture
def register_password():
    return get_random_string(12)


@pytest.mark.django_db
class TestRegistration:
    def test_register_natural_check_holder(
        self, api_client, check_holder_group, register_password,
    ):
        payload = {
            "username": "checkuser",
            "email": "check@example.com",
            "name": "Check User",
            "phone": "09123456789",
            "role": "check_holder",
            "user_type": "natural",
            "password": register_password,
            "password_confirm": register_password,
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["role"] == "check_holder"
        assert response.data["user"]["user_type"] == "natural"
        assert "access" in response.data
        assert "refresh" in response.data

        user = User.objects.get(username="checkuser")
        assert user.role == "check_holder"
        assert user.profile.user_type == Profile.UserType.NATURAL
        assert user.groups.filter(name="CheckHolder").exists()

    def test_register_legal_requires_company_name(
        self, api_client, check_holder_group, register_password,
    ):
        payload = {
            "username": "legalmissingname",
            "email": "legal@example.com",
            "role": "check_holder",
            "user_type": "legal",
            "password": register_password,
            "password_confirm": register_password,
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["code"] == "VALIDATION_ERROR"
        assert "name" in response.data["error"]["details"]

    def test_register_legal_success(
        self, api_client, investor_group, register_password,
    ):
        payload = {
            "username": "legaluser",
            "email": "legalok@example.com",
            "name": "Official Company Name",
            "role": "investor",
            "user_type": "legal",
            "password": register_password,
            "password_confirm": register_password,
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["user_type"] == "legal"
        assert response.data["user"]["name"] == "Official Company Name"

        user = User.objects.get(username="legaluser")
        assert user.profile.user_type == Profile.UserType.LEGAL
        assert user.groups.filter(name="Investor").exists()

    def test_register_missing_user_type(self, api_client, register_password):
        payload = {
            "username": "nousertype",
            "email": "nousertype@example.com",
            "role": "check_holder",
            "password": register_password,
            "password_confirm": register_password,
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"]["code"] == "VALIDATION_ERROR"

    def test_register_investor(self, api_client, investor_group, register_password):
        payload = {
            "username": "investoruser",
            "email": "invest@example.com",
            "name": "Investor User",
            "phone": "09129876543",
            "role": "investor",
            "user_type": "natural",
            "password": register_password,
            "password_confirm": register_password,
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["role"] == "investor"
        assert response.data["user"]["user_type"] == "natural"

        user = User.objects.get(username="investoruser")
        assert user.role == "investor"
        assert user.groups.filter(name="Investor").exists()

    def test_register_duplicate_username(self, api_client, check_holder_group, register_password):
        existing_password = get_random_string(12)
        User.objects.create_user(username="existing", password=existing_password)
        payload = {
            "username": "existing",
            "email": "new@example.com",
            "role": "check_holder",
            "user_type": "natural",
            "password": register_password,
            "password_confirm": register_password,
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_mismatch(self, api_client, register_password):
        payload = {
            "username": "mismatch",
            "email": "mismatch@example.com",
            "role": "investor",
            "user_type": "natural",
            "password": register_password,
            "password_confirm": get_random_string(12),
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_invalid_role(self, api_client, register_password):
        payload = {
            "username": "invalidrole",
            "email": "invalid@example.com",
            "role": "admin",
            "user_type": "natural",
            "password": register_password,
            "password_confirm": register_password,
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserMe:
    def test_get_current_user(self, api_client):
        password = get_random_string(12)
        user = User.objects.create_user(
            username="meuser",
            password=password,
            role="check_holder",
        )
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/users/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "meuser"
        assert response.data["role"] == "check_holder"
        assert response.data["user_type"] == "natural"

    def test_unauthenticated_access(self, api_client):
        response = api_client.get("/api/v1/users/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
