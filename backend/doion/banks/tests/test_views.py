import pytest
from rest_framework import status
from rest_framework.test import APIClient

from doion.banks.catalog import INITIAL_BANKS
from doion.banks.models import Bank
from doion.banks.seed import seed_catalog_banks
from doion.checks.factories import ChequeListingFactory
from doion.identity.factories import ProfileFactory
from doion.users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def catalog(db):
    seed_catalog_banks()
    return Bank.objects.all()


@pytest.mark.django_db
class TestBankCatalogAPI:
    def test_guest_list_returns_active_catalog(self, api_client, catalog):
        response = api_client.get("/api/v1/banks/")

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= len(INITIAL_BANKS)
        codes = {item["code"] for item in response.data}
        assert {row["code"] for row in INITIAL_BANKS} <= codes
        mellat = next(item for item in response.data if item["code"] == "mellat")
        assert mellat["display_name"] == "بانک ملت"
        assert "aliases" in mellat
        assert mellat["logo_url"] is None
        assert mellat["brand_color_light"].startswith("#")
        assert mellat["brand_color_dark"].startswith("#")

    def test_inactive_bank_is_omitted(self, api_client, catalog):
        Bank.objects.filter(code="sina").update(is_active=False)

        response = api_client.get("/api/v1/banks/")

        codes = {item["code"] for item in response.data}
        assert "sina" not in codes

    def test_post_is_not_allowed(self, api_client, catalog):
        response = api_client.post("/api/v1/banks/", {"code": "new"}, format="json")

        assert response.status_code in {
            status.HTTP_403_FORBIDDEN,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        }

    def test_retrieve_is_not_allowed(self, api_client, catalog):
        bank = Bank.objects.get(code="mellat")

        response = api_client.get(f"/api/v1/banks/{bank.pk}/")

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_list_is_ordered_by_display_name(self, api_client, catalog):
        response = api_client.get("/api/v1/banks/")

        names = [item["display_name"] for item in response.data]
        assert names == sorted(names)

    def test_empty_catalog_returns_empty_list(self, api_client, catalog):
        Bank.objects.update(is_active=False)

        response = api_client.get("/api/v1/banks/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []


@pytest.mark.django_db
class TestNestedBankOnListings:
    def test_retrieve_includes_nested_bank_or_null(self, api_client, catalog):
        user = UserFactory.create()
        ProfileFactory.create(user=user, role=user.role)
        mapped = ChequeListingFactory.create(owner=user)
        unknown = ChequeListingFactory.create(
            owner=user,
            bank=None,
            bank_name="بانک ساختگی",
            cheque_serial_number="1888888888888888",
        )
        api_client.force_authenticate(user=user)

        mapped_response = api_client.get(f"/api/v1/listings/{mapped.id}/")
        unknown_response = api_client.get(f"/api/v1/listings/{unknown.id}/")

        assert mapped_response.status_code == status.HTTP_200_OK
        assert mapped_response.data["bank"]["code"] == "mellat"
        assert mapped_response.data["bank_name"] == "بانک ملت"
        assert unknown_response.data["bank"] is None
        assert unknown_response.data["bank_name"] == "بانک ساختگی"
