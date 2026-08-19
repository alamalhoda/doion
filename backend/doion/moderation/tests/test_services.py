import pytest

from doion.checks.factories import ChequeListingFactory
from doion.checks.models import ChequeListing
from doion.moderation.constants import MAX_LISTING_RESUBMITS
from doion.moderation.exceptions import ModerationResubmitLimitExceeded
from doion.moderation.models import ModerationDecision
from doion.moderation.services import ModerationService
from doion.users.factories import UserFactory


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.mark.django_db
class TestModerationServiceApprove:
    def _create_listing(self, user, status=ChequeListing.Status.PENDING_MODERATION):
        return ChequeListingFactory.create(
            owner=user,
            status=status,
            bank_name="بانک ملت",
            face_amount=500000000,
            due_date="2026-12-31",
            issuer_type="legal",
            issuer_name="شرکت فناوری نوین",
        )

    def test_approve_pending_listing(self, user):
        listing = self._create_listing(user)

        decision = ModerationService.approve_listing(listing.id, user)

        listing.refresh_from_db()
        assert listing.status == ChequeListing.Status.PUBLISHED
        assert listing.rejection_reason == ""
        assert listing.rejection_code is None
        assert decision.decision == ModerationDecision.Decision.APPROVED

    def test_approve_non_pending_raises(self, user):
        listing = self._create_listing(user, status=ChequeListing.Status.PUBLISHED)

        with pytest.raises(ValueError, match="not in pending moderation"):
            ModerationService.approve_listing(listing.id, user)


@pytest.mark.django_db
class TestModerationServiceReject:
    def _create_listing(self, user, status=ChequeListing.Status.PENDING_MODERATION, resubmit_count=0):
        return ChequeListingFactory.create(
            owner=user,
            status=status,
            resubmit_count=resubmit_count,
            bank_name="بانک ملت",
            face_amount=500000000,
            due_date="2026-12-31",
            issuer_type="legal",
            issuer_name="شرکت فناوری نوین",
        )

    def test_reject_first_time(self, user):
        listing = self._create_listing(user)

        decision = ModerationService.reject_listing(
            listing.id, user, "MOD_101", "اطلاعات ناقص",
        )

        listing.refresh_from_db()
        assert listing.status == ChequeListing.Status.REJECTED
        assert listing.rejection_code == "MOD_101"
        assert listing.rejection_reason == "اطلاعات ناقص"
        assert listing.resubmit_count == 1
        assert decision.decision == ModerationDecision.Decision.REJECTED

    def test_reject_already_rejected_increments(self, user):
        listing = self._create_listing(
            user, status=ChequeListing.Status.REJECTED, resubmit_count=1,
        )

        ModerationService.reject_listing(
            listing.id, user, "MOD_102", "تصویر بی کیفیت",
        )

        listing.refresh_from_db()
        assert listing.resubmit_count == MAX_LISTING_RESUBMITS - 1

    def test_reject_after_three_resubmits_raises_mod_306(self, user):
        listing = self._create_listing(
            user, status=ChequeListing.Status.PENDING_MODERATION, resubmit_count=MAX_LISTING_RESUBMITS,
        )

        with pytest.raises(ModerationResubmitLimitExceeded) as exc_info:
            ModerationService.reject_listing(
                listing.id, user, "MOD_101", "reject again",
            )

        assert exc_info.value.default_code == "MOD_306"

        listing.refresh_from_db()
        assert listing.resubmit_count == MAX_LISTING_RESUBMITS

    def test_reject_non_pending_raises(self, user):
        listing = self._create_listing(user, status=ChequeListing.Status.PUBLISHED)

        with pytest.raises(ValueError, match="not in pending moderation"):
            ModerationService.reject_listing(
                listing.id, user, "MOD_101", "should fail",
            )
