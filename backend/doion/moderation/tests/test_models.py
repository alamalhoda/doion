import pytest

from doion.moderation.models import ModerationDecision


@pytest.mark.django_db
class TestModerationDecisionModel:
    def test_create_approved_decision(self, user):
        from doion.checks.models import ChequeListing, IssuerProfile

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
        )

        decision = ModerationDecision.objects.create(
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
        from doion.checks.models import ChequeListing, IssuerProfile

        issuer = IssuerProfile.objects.create(
            national_or_company_id="0987654321",
            name="Test Issuer 2",
        )
        listing = ChequeListing.objects.create(
            owner=user,
            issuer=issuer,
            bank_name="بانک ملت",
            cheque_serial_number="6543210987654321",
            face_amount=100000000,
            due_date="2026-12-31",
            issuer_type="natural",
            issuer_name="رضا کریمی",
            issuer_national_id="0012345678",
        )

        decision = ModerationDecision.objects.create(
            listing=listing,
            moderator=user,
            decision=ModerationDecision.Decision.REJECTED,
            rejection_code="MOD_101",
            rejection_note="اطلاعات ناقص",
        )

        assert decision.decision == "rejected"
        assert decision.rejection_code == "MOD_101"
        assert decision.rejection_note == "اطلاعات ناقص"

    def test_listing_related_name(self, user):
        from doion.checks.models import ChequeListing, IssuerProfile

        issuer = IssuerProfile.objects.create(
            national_or_company_id="1122334455",
            name="Test Issuer 3",
        )
        listing = ChequeListing.objects.create(
            owner=user,
            issuer=issuer,
            bank_name="بانک صادرات",
            cheque_serial_number="1111222233334444",
            face_amount=200000000,
            due_date="2026-12-31",
            issuer_type="legal",
            issuer_name="شرکت آزمایشی",
            issuer_national_id="1122334455",
        )

        ModerationDecision.objects.create(
            listing=listing,
            moderator=user,
            decision=ModerationDecision.Decision.APPROVED,
        )
        ModerationDecision.objects.create(
            listing=listing,
            moderator=user,
            decision=ModerationDecision.Decision.REJECTED,
            rejection_code="MOD_102",
        )

        assert listing.moderation_decisions.count() == 2
