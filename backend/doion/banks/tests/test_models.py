import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction

from doion.banks.catalog import INITIAL_BANKS
from doion.banks.factories import BankFactory
from doion.banks.models import Bank
from doion.banks.seed import seed_catalog_banks
from doion.checks.factories import ChequeListingFactory


@pytest.mark.django_db
class TestBankModel:
    def test_code_must_be_unique(self):
        BankFactory.create(code="unique-bank")

        with pytest.raises(IntegrityError), transaction.atomic():
            BankFactory.create(code="unique-bank", display_name="بانک دیگر")

    def test_alias_must_be_unique_across_catalog(self):
        BankFactory.create(
            code="alpha",
            display_name="بانک آلفا",
            aliases=["بانک آلفا"],
        )
        other = BankFactory.build(
            code="beta",
            display_name="بانک بتا",
            aliases=["بانک بتا", "بانک آلفا"],
        )

        with pytest.raises(ValidationError) as exc_info:
            other.full_clean()

        assert "aliases" in exc_info.value.error_dict

    def test_aliases_must_include_display_name(self):
        bank = BankFactory.build(
            code="gamma",
            display_name="بانک گاما",
            aliases=["گاما"],
        )

        with pytest.raises(ValidationError) as exc_info:
            bank.full_clean()

        assert "aliases" in exc_info.value.error_dict

    def test_code_cannot_change_after_create(self):
        bank = BankFactory.create(code="locked")
        bank.code = "changed"

        with pytest.raises(ValidationError) as exc_info:
            bank.save()

        assert "code" in exc_info.value.error_dict
        bank.refresh_from_db()
        assert bank.code == "locked"

    def test_brand_colors_must_be_hex(self):
        bank = BankFactory.build(brand_color_light="red", brand_color_dark="#112233")

        with pytest.raises(ValidationError) as exc_info:
            bank.full_clean()

        assert "brand_color_light" in exc_info.value.error_dict


@pytest.mark.django_db
class TestBankCatalogSeed:
    def test_seed_creates_at_least_fourteen_banks(self):
        created = seed_catalog_banks()

        assert Bank.objects.count() >= len(INITIAL_BANKS)
        assert created in {0, len(INITIAL_BANKS)}
        codes = set(Bank.objects.values_list("code", flat=True))
        expected_codes = {row["code"] for row in INITIAL_BANKS}
        assert expected_codes <= codes

    def test_seed_is_idempotent(self):
        seed_catalog_banks()
        count_after_first = Bank.objects.count()

        created = seed_catalog_banks()

        assert created == 0
        assert Bank.objects.count() == count_after_first

    def test_seed_does_not_overwrite_existing_row(self):
        seed_catalog_banks()
        bank = Bank.objects.get(code="mellat")
        bank.brand_color_light = "#111111"
        bank.save()

        seed_catalog_banks()

        bank.refresh_from_db()
        assert bank.brand_color_light == "#111111"


@pytest.mark.django_db
class TestChequeListingBankFk:
    def test_listing_bank_fk_is_nullable(self):
        listing = ChequeListingFactory.create(bank=None)

        assert listing.bank_id is None
        listing.refresh_from_db()
        assert listing.bank_id is None
