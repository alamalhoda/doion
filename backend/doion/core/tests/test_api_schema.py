"""Smoke contract test: critical paths exist in OpenAPI schema."""

import pytest
from rest_framework.test import APIClient

from doion.users.factories import UserFactory

CRITICAL_PATH_FRAGMENTS = (
    "/api/v1/listings/",
    "/api/v1/matches/",
    "/api/v1/auth/login/",
    "/api/v1/marketplace/listings/",
    "/api/v1/moderation/",
)


@pytest.mark.django_db
def test_openapi_schema_includes_critical_paths():
    client = APIClient()
    client.force_authenticate(user=UserFactory.create(as_admin=True))
    response = client.get("/api/v1/schema/")

    assert response.status_code == 200
    schema_text = response.content.decode("utf-8")
    for fragment in CRITICAL_PATH_FRAGMENTS:
        assert fragment in schema_text, f"Missing schema path fragment: {fragment}"
