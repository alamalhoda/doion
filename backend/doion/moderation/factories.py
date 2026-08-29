"""Moderation factories for tests and demo seeding."""

from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from doion.checks.factories import ChequeListingFactory
from doion.moderation.constants import RejectionCode
from doion.moderation.models import ModerationDecision
from doion.users.factories import UserFactory


class ModerationDecisionFactory(DjangoModelFactory):
    class Meta:
        model = ModerationDecision

    listing = factory.SubFactory(ChequeListingFactory, pending=True)
    moderator = factory.SubFactory(UserFactory, as_moderator=True)
    decision = ModerationDecision.Decision.APPROVED
    rejection_code = None
    rejection_note = ""

    class Params:
        as_rejected = factory.Trait(
            decision=ModerationDecision.Decision.REJECTED,
            rejection_code=RejectionCode.INCOMPLETE_INFO,
            rejection_note="Incomplete information",
        )
