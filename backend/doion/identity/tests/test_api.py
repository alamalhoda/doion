import pytest
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APIClient

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


@pytest.mark.django_db
class TestRegistration:
    def test_register_check_holder(self, api_client, check_holder_group):
        payload = {
            "username": "checkuser",
            "email": "check@example.com",
            "name": "Check User",
            "phone": "09123456789",
            "role": "check_holder",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["role"] == "check_holder"
        assert "access" in response.data
        assert "refresh" in response.data

        user = User.objects.get(username="checkuser")
        assert user.role == "check_holder"
        assert user.groups.filter(name="CheckHolder").exists()

    def test_register_investor(self, api_client, investor_group):
        payload = {
            "username": "investoruser",
            "email": "invest@example.com",
            "name": "Investor User",
            "phone": "09129876543",
            "role": "investor",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["role"] == "investor"

        user = User.objects.get(username="investoruser")
        assert user.role == "investor"
        assert user.groups.filter(name="Investor").exists()

    def test_register_duplicate_username(self, api_client, check_holder_group):
        User.objects.create_user(username="existing", password="testpass123")
        payload = {
            "username": "existing",
            "email": "new@example.com",
            "role": "check_holder",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_mismatch(self, api_client):
        payload = {
            "username": "mismatch",
            "email": "mismatch@example.com",
            "role": "investor",
            "password": "securepass123",
            "password_confirm": "different123",
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_invalid_role(self, api_client):
        payload = {
            "username": "invalidrole",
            "email": "invalid@example.com",
            "role": "admin",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        response = api_client.post("/api/v1/identity/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserMe:
    def test_get_current_user(self, api_client):
        user = User.objects.create_user(username="meuser", password="testpass123", role="check_holder")
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/users/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == "meuser"
        assert response.data["role"] == "check_holder"

    def test_unauthenticated_access(self, api_client):
        response = api_client.get("/api/v1/users/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
