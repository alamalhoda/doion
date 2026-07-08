import pytest
from rest_framework.test import APIClient

from doion.compliance.models import FeatureFlag
from doion.users.tests.factories import UserFactory

BASE = "/api/v1/compliance"


@pytest.fixture
def moderator(db):
    return UserFactory.create(role="moderator")


@pytest.fixture
def admin(db):
    return UserFactory.create(role="admin")


@pytest.fixture
def normal_user(db):
    return UserFactory.create(role="investor")


@pytest.mark.django_db
class TestFeatureFlagEndpoints:
    def test_moderator_can_list_flags(self, moderator):
        FeatureFlag.objects.create(key="some_flag", is_enabled=True)
        client = APIClient()
        client.force_authenticate(user=moderator)
        resp = client.get(f"{BASE}/feature-flags/")
        assert resp.status_code == 200
        assert resp.data["count"] >= 1

    def test_matching_enabled_seed_present(self, admin):
        flag, _ = FeatureFlag.objects.get_or_create(
            key="matching_enabled", defaults={"is_enabled": True}
        )
        client = APIClient()
        client.force_authenticate(user=admin)
        resp = client.get(f"{BASE}/feature-flags/matching_enabled/")
        assert resp.status_code == 200
        assert resp.data["key"] == "matching_enabled"
        assert resp.data["is_enabled"] == flag.is_enabled

    def test_patch_flag_toggles_value(self, admin):
        FeatureFlag.objects.create(key="toggle_me", is_enabled=False)
        client = APIClient()
        client.force_authenticate(user=admin)
        resp = client.patch(
            f"{BASE}/feature-flags/toggle_me/",
            {"is_enabled": True},
            format="json",
        )
        assert resp.status_code == 200
        flag = FeatureFlag.objects.get(key="toggle_me")
        assert flag.is_enabled is True

    def test_system_flag_cannot_be_patched(self, admin):
        FeatureFlag.objects.create(key="sys_flag", is_enabled=True, is_system=True)
        client = APIClient()
        client.force_authenticate(user=admin)
        resp = client.patch(
            f"{BASE}/feature-flags/sys_flag/",
            {"is_enabled": False},
            format="json",
        )
        assert resp.status_code == 403

    def test_normal_user_denied(self, normal_user):
        client = APIClient()
        client.force_authenticate(user=normal_user)
        resp = client.get(f"{BASE}/feature-flags/")
        assert resp.status_code in (403, 401)


@pytest.mark.django_db
class TestComplianceStats:
    def test_stats_returns_expected_keys(self, admin):
        client = APIClient()
        client.force_authenticate(user=admin)
        resp = client.get(f"{BASE}/stats/")
        assert resp.status_code == 200
        data = resp.data
        for top in ("listings", "users", "verifications", "notifications"):
            assert top in data
        for key in ("total", "published", "pending_moderation", "rejected"):
            assert key in data["listings"]
