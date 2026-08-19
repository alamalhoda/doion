"""Bank factories for tests and demo seeding."""

from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from doion.banks.models import Bank


class BankFactory(DjangoModelFactory):
    class Meta:
        model = Bank

    code = factory.Sequence(lambda n: f"bank-{n}")
    display_name = factory.LazyAttribute(lambda o: f"بانک {o.code}")
    aliases = factory.LazyAttribute(lambda o: [o.display_name])
    brand_color_light = "#3366CC"
    brand_color_dark = "#224499"
    is_active = True
