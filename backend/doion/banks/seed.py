"""Idempotent seed of the initial bank catalog."""

from __future__ import annotations

from doion.banks.catalog import INITIAL_BANKS
from doion.banks.models import Bank


def seed_catalog_banks() -> int:
    created_count = 0
    for row in INITIAL_BANKS:
        _, created = Bank.objects.get_or_create(
            code=row["code"],
            defaults={
                "display_name": row["display_name"],
                "aliases": list(row["aliases"]),
                "brand_color_light": row["brand_color_light"],
                "brand_color_dark": row["brand_color_dark"],
                "is_active": True,
            },
        )
        if created:
            created_count += 1
    return created_count


def seed_catalog_banks_on_migrate(**kwargs) -> None:
    seed_catalog_banks()
