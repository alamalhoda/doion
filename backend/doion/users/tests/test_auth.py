"""API tests for JWT login and refresh endpoints."""

import pytest
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_password():
    return get_random_string(12)


@pytest.fixture
def user(db, user_password):
    return UserFactory.create(password=user_password)


@pytest.mark.django_db
class TestAuthLogin:
    def test_login_with_username_returns_tokens(self, api_client, user, user_password):
        response = api_client.post(
            "/api/v1/auth/login/",
            {"identifier": user.username, "password": user_password},
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["username"] == user.username
        assert response.data["user"]["role"] == user.role

    def test_login_with_wrong_password_returns_401(self, api_client, user):
        response = api_client.post(
            "/api/v1/auth/login/",
            {"identifier": user.username, "password": get_random_string(12)},
            format="json",
        )

        assert response.status_code == 401

    def test_login_with_unknown_identifier_returns_401(self, api_client):
        response = api_client.post(
            "/api/v1/auth/login/",
            {"identifier": "missing-user", "password": get_random_string(12)},
            format="json",
        )

        assert response.status_code == 401


@pytest.mark.django_db
class TestAuthRefresh:
    def test_refresh_with_valid_token_returns_new_tokens(self, api_client, user):
        refresh = RefreshToken.for_user(user)

        response = api_client.post(
            "/api/v1/auth/refresh/",
            {"refresh": str(refresh)},
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["id"] == user.id

    def test_refresh_with_invalid_token_returns_401(self, api_client):
        response = api_client.post(
            "/api/v1/auth/refresh/",
            {"refresh": "not-a-valid-token"},
            format="json",
        )

        assert response.status_code == 401
