"""Bank catalog domain services."""

from __future__ import annotations

from doion.banks.models import Bank
from doion.banks.seed import seed_catalog_banks
from doion.checks.models import ChequeListing

BANK_NAME_NOT_ACCEPTED = "Send catalog bank code in 'bank'; bank_name is not accepted."
UNKNOWN_OR_INACTIVE_BANK_CODE = "Unknown or inactive bank code."


class UnknownOrInactiveBankError(LookupError):
    """Raised when a write path receives a missing or inactive bank code."""


def get_active_by_code(code: str) -> Bank:
    normalized = code.strip()
    if not normalized:
        raise UnknownOrInactiveBankError(UNKNOWN_OR_INACTIVE_BANK_CODE)
    bank = Bank.objects.filter(code=normalized, is_active=True).first()
    if bank is None:
        raise UnknownOrInactiveBankError(UNKNOWN_OR_INACTIVE_BANK_CODE)
    return bank


def match_bank_from_legacy_name(name: str, banks: list[Bank]) -> Bank | None:
    needle = name.strip()
    if not needle:
        return None
    for bank in banks:
        aliases = bank.aliases if isinstance(bank.aliases, list) else []
        candidates = [bank.display_name, *aliases]
        if any(str(item).strip() == needle for item in candidates):
            return bank
    return None


def resolve_legacy_name(name: str) -> Bank | None:
    return match_bank_from_legacy_name(name, list(Bank.objects.all()))


def apply_bank_to_listing(listing: ChequeListing, bank: Bank) -> ChequeListing:
    listing.bank = bank
    listing.bank_name = bank.display_name
    return listing


def backfill_listing_banks() -> dict[str, int]:
    seed_catalog_banks()
    banks = list(Bank.objects.all())
    mapped = 0
    unmatched = 0
    listings = ChequeListing.objects.filter(bank__isnull=True)
    for listing in listings.iterator():
        bank = match_bank_from_legacy_name(listing.bank_name, banks)
        if bank is None:
            unmatched += 1
            continue
        apply_bank_to_listing(listing, bank)
        listing.save(update_fields=["bank", "bank_name", "updated_at"])
        mapped += 1
    return {"mapped": mapped, "unmatched": unmatched}
