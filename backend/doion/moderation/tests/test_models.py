import pytest

from doion.checks.factories import ChequeListingFactory
from doion.moderation.factories import ModerationDecisionFactory
from doion.moderation.models import ModerationDecision
from doion.users.factories import UserFactory


@pytest.mark.django_db
class TestModerationDecisionModel:
    def test_create_approved_decision(self, user):
        listing = ChequeListingFactory.create(owner=user)
        decision = ModerationDecisionFactory.create(
            listing=listing,
            moderator=user,
            decision=ModerationDecision.Decision.APPROVED,
        )

        assert decision.id is not None
        assert decision.decision == "approved"
        assert decision.listing == listing
        assert decision.moderator == user
        assert decision.rejection_code is None
        assert decision.rejection_note == ""

    def test_create_rejected_decision(self, user):
        listing = ChequeListingFactory.create(
            owner=user,
            issuer_type="natural",
            issuer_name="رضا کریمی",
        )
        decision = ModerationDecisionFactory.create(
            as_rejected=True,
            listing=listing,
            moderator=user,
            rejection_note="اطلاعات ناقص",
        )

        assert decision.decision == "rejected"
        assert decision.rejection_code == "MOD_101"
        assert decision.rejection_note == "اطلاعات ناقص"

    def test_listing_related_name(self, user):
        listing = ChequeListingFactory.create(
            owner=user,
            bank_name="بانک صادرات",
        )
        ModerationDecisionFactory.create(
            listing=listing,
            moderator=user,
            decision=ModerationDecision.Decision.APPROVED,
        )
        ModerationDecisionFactory.create(
            as_rejected=True,
            listing=listing,
            moderator=user,
            rejection_code="MOD_102",
        )

        assert listing.moderation_decisions.count() == 2
