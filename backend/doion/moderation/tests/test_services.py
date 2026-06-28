import pytest

from doion.checks.models import ChequeListing
from doion.moderation.exceptions import ModerationResubmitLimitExceeded
from doion.moderation.models import ModerationDecision
from doion.moderation.services import ModerationService
from doion.users.tests.factories import UserFactory


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.mark.django_db
class TestModerationServiceApprove:
    def _create_listing(self, user, status=ChequeListing.Status.PENDING_MODERATION):
        from doion.checks.models import IssuerProfile

        issuer = IssuerProfile.objects.create(
            national_or_company_id="1234567890",
            name="Test Issuer",
        )
        listing = ChequeListing.objects.create(
            owner=user,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="1234567890123456",
            face_amount=500000000,
            due_date="2026-12-31",
            issuer_type="legal",
            issuer_name="شرکت فناوری نوین",
            issuer_national_id="1234567890",
            status=status,
        )
        return listing

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
        from doion.checks.models import IssuerProfile

        issuer = IssuerProfile.objects.create(
            national_or_company_id="1234567890",
            name="Test Issuer",
        )
        listing = ChequeListing.objects.create(
            owner=user,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="1234567890123456",
            face_amount=500000000,
            due_date="2026-12-31",
            issuer_type="legal",
            issuer_name="شرکت فناوری نوین",
            issuer_national_id="1234567890",
            status=status,
            resubmit_count=resubmit_count,
        )
        return listing

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
        assert listing.resubmit_count == 2

    def test_reject_after_three_resubmits_raises_mod_306(self, user):
        listing = self._create_listing(
            user, status=ChequeListing.Status.PENDING_MODERATION, resubmit_count=3,
        )

        with pytest.raises(ModerationResubmitLimitExceeded) as exc_info:
            ModerationService.reject_listing(
                listing.id, user, "MOD_101", "reject again",
            )

        assert exc_info.value.default_code == "MOD_306"

        listing.refresh_from_db()
        assert listing.resubmit_count == 3

    def test_reject_non_pending_raises(self, user):
        listing = self._create_listing(user, status=ChequeListing.Status.PUBLISHED)

        with pytest.raises(ValueError, match="not in pending moderation"):
            ModerationService.reject_listing(
                listing.id, user, "MOD_101", "should fail",
            )
