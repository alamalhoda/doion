import pytest

from doion.banks.factories import BankFactory
from doion.banks.models import Bank
from doion.banks.seed import seed_catalog_banks
from doion.banks.services import UnknownOrInactiveBankError
from doion.banks.services import apply_bank_to_listing
from doion.banks.services import backfill_listing_banks
from doion.banks.services import get_active_by_code
from doion.banks.services import resolve_legacy_name
from doion.checks.factories import ChequeListingFactory


@pytest.mark.django_db
class TestBankCatalogServices:
    def test_get_active_by_code_returns_catalog_bank(self):
        seed_catalog_banks()

        bank = get_active_by_code("mellat")

        assert bank.code == "mellat"
        assert bank.display_name == "بانک ملت"

    def test_get_active_by_code_rejects_inactive_bank(self):
        bank = BankFactory.create(code="frozen", is_active=False)

        with pytest.raises(UnknownOrInactiveBankError):
            get_active_by_code(bank.code)

    def test_resolve_legacy_name_matches_alias(self):
        seed_catalog_banks()

        bank = resolve_legacy_name("  بانک ملی  ")

        assert bank is not None
        assert bank.code == "melli"
        assert bank.display_name == "بانک ملی ایران"

    def test_resolve_legacy_name_unknown_returns_none(self):
        seed_catalog_banks()

        assert resolve_legacy_name("بانک ساختگی") is None

    def test_apply_bank_to_listing_sets_fk_and_display_name(self):
        seed_catalog_banks()
        mellat = Bank.objects.get(code="mellat")
        listing = ChequeListingFactory.build(bank=None, bank_name="old")

        apply_bank_to_listing(listing, mellat)

        assert listing.bank == mellat
        assert listing.bank_name == "بانک ملت"

    def test_backfill_maps_alias_and_leaves_unknown_null(self):
        seed_catalog_banks()
        mapped = ChequeListingFactory.create(
            bank=None,
            bank_name="بانک ملی",
        )
        unknown = ChequeListingFactory.create(
            bank=None,
            bank_name="بانک ساختگی",
            cheque_serial_number="1999999999999999",
        )

        result = backfill_listing_banks()

        mapped.refresh_from_db()
        unknown.refresh_from_db()
        assert mapped.bank is not None
        assert mapped.bank.code == "melli"
        assert mapped.bank_name == "بانک ملی ایران"
        assert unknown.bank_id is None
        assert unknown.bank_name == "بانک ساختگی"
        assert result["mapped"] >= 1
        assert result["unmatched"] >= 1
