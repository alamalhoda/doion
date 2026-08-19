"""Smoke tests for domain factories used by tests and future demo seeding."""

import pytest

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.identity.factories import ProfileFactory
from doion.identity.factories import VerificationFactory
from doion.matching.constants import Status
from doion.matching.factories import MatchFactory
from doion.moderation.factories import ModerationDecisionFactory
from doion.moderation.models import ModerationDecision
from doion.notifications.factories import NotificationFactory
from doion.users.factories import UserFactory
from doion.users.models import User


@pytest.mark.django_db
class TestDomainFactories:
    def test_user_role_traits(self):
        assert UserFactory.create().role == User.Role.CHECK_HOLDER
        assert UserFactory.create(as_investor=True).role == User.Role.INVESTOR
        assert UserFactory.create(as_moderator=True).role == User.Role.MODERATOR
        assert UserFactory.create(as_admin=True).role == User.Role.ADMIN

    def test_cheque_listing_traits(self):
        issuer = IssuerProfileFactory.create()
        published = ChequeListingFactory.create(published=True, issuer=issuer)
        pending = ChequeListingFactory.create(pending=True)
        assert published.status == ChequeListing.Status.PUBLISHED
        assert pending.status == ChequeListing.Status.PENDING_MODERATION

    def test_identity_and_notification_factories(self):
        user = UserFactory.create()
        profile = ProfileFactory.create(user=user, verified=True)
        verification = VerificationFactory.create(user=user)
        notification = NotificationFactory.create(user=user)
        assert profile.is_verified is True
        assert verification.status == "pending"
        assert notification.user == user

    def test_match_and_moderation_factories(self):
        match = MatchFactory.create()
        decision = ModerationDecisionFactory.create()
        rejected = ModerationDecisionFactory.create(as_rejected=True)
        assert match.status == Status.PENDING
        assert match.check_holder == match.listing.owner
        assert decision.decision == ModerationDecision.Decision.APPROVED
        assert rejected.decision == ModerationDecision.Decision.REJECTED
