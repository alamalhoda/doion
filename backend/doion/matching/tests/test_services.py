import pytest

from doion.checks.factories import ChequeListingFactory
from doion.checks.factories import IssuerProfileFactory
from doion.checks.models import ChequeListing
from doion.matching.constants import Status
from doion.matching.exceptions import InvalidMatchStatus, MatchNotAllowed
from doion.matching.models import OffPlatformSettlement
from doion.matching.services import MatchingService
from doion.users.factories import UserFactory


@pytest.fixture
def investor(db):
    return UserFactory.create(as_investor=True)


@pytest.fixture
def check_holder(db):
    return UserFactory.create()


@pytest.fixture
def other_check_holder(db):
    return UserFactory.create()


@pytest.fixture
def issuer(db):
    return IssuerProfileFactory.create(
        national_or_company_id="1234567890",
        name="Test Issuer",
    )


def create_listing(owner, **kwargs):
    defaults = {
        "owner": owner,
        "bank_name": "Bank Melli",
        "issuer_type": "legal",
        "issuer_name": "Test Corp",
        "issuer_national_id": "987654321",
        "status": ChequeListing.Status.PUBLISHED,
    }
    if "issuer" not in kwargs:
        defaults["issuer"] = IssuerProfileFactory.create(
            national_or_company_id="1234567890",
            name="Test Issuer",
        )
    defaults.update(kwargs)
    return ChequeListingFactory.create(**defaults)


@pytest.mark.django_db
class TestMatchingServiceCreateMatch:
    def test_create_match_success(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)

        match = MatchingService.create_match(listing.id, investor)

        assert match.listing == listing
        assert match.investor == investor
        assert match.check_holder == check_holder
        assert match.status == Status.PENDING
        assert match.settlement_type == "off_platform"

    def test_create_match_not_published(self, investor, check_holder, issuer):
        listing = create_listing(
            owner=check_holder,
            issuer=issuer,
            status=ChequeListing.Status.PENDING_MODERATION,
        )

        with pytest.raises(MatchNotAllowed, match="Listing is not published"):
            MatchingService.create_match(listing.id, investor)

    def test_create_match_own_listing(self, issuer):
        investor_owner = UserFactory.create(as_investor=True)
        listing = create_listing(owner=investor_owner, issuer=issuer)

        with pytest.raises(MatchNotAllowed, match="You cannot match your own listing"):
            MatchingService.create_match(listing.id, investor_owner)

    def test_create_match_non_investor(self, check_holder, issuer):
        not_investor = UserFactory.create()
        listing = create_listing(owner=check_holder, issuer=issuer)

        with pytest.raises(MatchNotAllowed, match="Only investors can create matches"):
            MatchingService.create_match(listing.id, not_investor)


@pytest.mark.django_db
class TestMatchingServiceAcceptMatch:
    def test_accept_match_success(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        accepted = MatchingService.accept_match(match.id, check_holder)

        assert accepted.status == Status.ACCEPTED

        listing.refresh_from_db()
        assert listing.status == ChequeListing.Status.MATCHED

    def test_accept_match_not_pending(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)
        match.status = Status.ACCEPTED
        match.save()

        with pytest.raises(InvalidMatchStatus, match="Match is not pending"):
            MatchingService.accept_match(match.id, check_holder)

    def test_accept_match_not_holder(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        wrong_user = UserFactory.create()
        with pytest.raises(MatchNotAllowed, match="not authorized to accept"):
            MatchingService.accept_match(match.id, wrong_user)


@pytest.mark.django_db
class TestMatchingServiceDeclineMatch:
    def test_decline_match_success(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        declined = MatchingService.decline_match(match.id, check_holder, note="not interested")

        assert declined.status == Status.DECLINED
        assert declined.message == "not interested"

    def test_decline_match_not_pending(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)
        match.status = Status.ACCEPTED
        match.save()

        with pytest.raises(InvalidMatchStatus, match="Match is not pending"):
            MatchingService.decline_match(match.id, check_holder)

    def test_decline_match_not_holder(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        wrong_user = UserFactory.create()
        with pytest.raises(MatchNotAllowed, match="not authorized to decline"):
            MatchingService.decline_match(match.id, wrong_user)


@pytest.mark.django_db
class TestMatchingServiceCancelMatch:
    def test_cancel_match_by_investor(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        cancelled = MatchingService.cancel_match(match.id, investor)

        assert cancelled.status == Status.CANCELLED

    def test_cancel_match_by_holder(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        cancelled = MatchingService.cancel_match(match.id, check_holder)

        assert cancelled.status == Status.CANCELLED

    def test_cancel_match_not_party(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        third_party = UserFactory.create()
        with pytest.raises(MatchNotAllowed, match="not a party"):
            MatchingService.cancel_match(match.id, third_party)

    def test_cancel_match_wrong_status(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)
        match.status = Status.DECLINED
        match.save()

        with pytest.raises(InvalidMatchStatus, match="cannot be cancelled"):
            MatchingService.cancel_match(match.id, investor)

    def test_cancel_match_reverts_listing_status(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)
        accepted = MatchingService.accept_match(match.id, check_holder)

        cancelled = MatchingService.cancel_match(accepted.id, investor)

        listing.refresh_from_db()
        assert listing.status == ChequeListing.Status.PUBLISHED


@pytest.mark.django_db
class TestMatchingServiceConfirmOffPlatform:
    def test_confirm_off_platform_success(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)
        accepted = MatchingService.accept_match(match.id, check_holder)

        confirmed = MatchingService.confirm_off_platform(accepted.id, check_holder)

        assert confirmed.status == Status.OFF_PLATFORM_CONFIRMED

        settlement = OffPlatformSettlement.objects.get(match=confirmed)
        assert settlement.confirmed_by == check_holder
        assert settlement.confirmed_at is not None

    def test_confirm_off_platform_not_accepted(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)

        with pytest.raises(InvalidMatchStatus, match="must be accepted"):
            MatchingService.confirm_off_platform(match.id, check_holder)

    def test_confirm_off_platform_not_holder(self, investor, check_holder, issuer):
        listing = create_listing(owner=check_holder, issuer=issuer)
        match = MatchingService.create_match(listing.id, investor)
        accepted = MatchingService.accept_match(match.id, check_holder)

        wrong_user = UserFactory.create()
        with pytest.raises(MatchNotAllowed, match="Only the check holder"):
            MatchingService.confirm_off_platform(accepted.id, wrong_user)
