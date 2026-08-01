"""Matching factories for tests and demo seeding."""

from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from doion.checks.factories import ChequeListingFactory
from doion.checks.models import ChequeListing
from doion.matching.constants import SettlementType
from doion.matching.constants import Status
from doion.matching.models import Match
from doion.users.factories import UserFactory
from doion.users.models import User


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    listing = factory.SubFactory(
        ChequeListingFactory,
        status=ChequeListing.Status.PUBLISHED,
        owner=factory.SubFactory(UserFactory, role=User.Role.CHECK_HOLDER),
    )
    investor = factory.SubFactory(UserFactory, as_investor=True)
    check_holder = factory.LazyAttribute(lambda o: o.listing.owner)
    status = Status.PENDING
    settlement_type = SettlementType.OFF_PLATFORM
    final_discount_rate = None
    terms = ""
    message = ""

    class Params:
        accepted = factory.Trait(status=Status.ACCEPTED)
        declined = factory.Trait(status=Status.DECLINED)
