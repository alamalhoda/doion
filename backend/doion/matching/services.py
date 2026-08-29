from django.db import transaction
from django.utils import timezone

from doion.checks.models import ChequeListing
from doion.matching.constants import SettlementType
from doion.matching.constants import Status
from doion.matching.exceptions import InvalidMatchStatus
from doion.matching.exceptions import MatchNotAllowed
from doion.matching.models import Match
from doion.matching.models import OffPlatformSettlement
from doion.matching.signals import MatchAccepted
from doion.matching.signals import MatchCancelled
from doion.matching.signals import MatchCreated
from doion.matching.signals import MatchDeclined
from doion.matching.signals import SettlementConfirmed


class MatchingService:
    @staticmethod
    def create_match(listing_id, investor):
        with transaction.atomic():
            listing = ChequeListing.objects.select_for_update().get(id=listing_id)

            if listing.status != ChequeListing.Status.PUBLISHED:
                msg = "Listing is not published"
                raise MatchNotAllowed(msg)

            if getattr(investor, "role", None) != "investor":
                msg = "Only investors can create matches"
                raise MatchNotAllowed(msg)

            if listing.owner_id == investor.id:
                msg = "You cannot match your own listing"
                raise MatchNotAllowed(msg)

            match = Match.objects.create(
                listing=listing,
                investor=investor,
                check_holder=listing.owner,
                status=Status.PENDING,
                settlement_type=SettlementType.OFF_PLATFORM,
            )

            MatchCreated.send(sender=Match, match=match, user=investor)

            return match

    @staticmethod
    def accept_match(match_id, check_holder):
        with transaction.atomic():
            match = Match.objects.select_for_update().get(id=match_id)

            if match.status != Status.PENDING:
                msg = "Match is not pending"
                raise InvalidMatchStatus(msg)

            if match.check_holder_id != check_holder.id:
                msg = "You are not authorized to accept this match"
                raise MatchNotAllowed(msg)

            match.status = Status.ACCEPTED
            match.save(update_fields=["status", "updated_at"])

            listing = match.listing
            listing.status = ChequeListing.Status.MATCHED
            listing.save(update_fields=["status", "updated_at"])

            MatchAccepted.send(sender=Match, match=match, user=check_holder)

            return match

    @staticmethod
    def decline_match(match_id, check_holder, note=""):
        with transaction.atomic():
            match = Match.objects.select_for_update().get(id=match_id)

            if match.status != Status.PENDING:
                msg = "Match is not pending"
                raise InvalidMatchStatus(msg)

            if match.check_holder_id != check_holder.id:
                msg = "You are not authorized to decline this match"
                raise MatchNotAllowed(msg)

            match.status = Status.DECLINED
            if note:
                match.message = note
            match.save(update_fields=["status", "message", "updated_at"])

            MatchDeclined.send(sender=Match, match=match, user=check_holder)

            return match

    @staticmethod
    def cancel_match(match_id, user):
        with transaction.atomic():
            match = Match.objects.select_for_update().get(id=match_id)

            if user.id not in (match.investor_id, match.check_holder_id):
                msg = "You are not a party to this match"
                raise MatchNotAllowed(msg)

            if match.status not in (Status.PENDING, Status.ACCEPTED):
                msg = "Match cannot be cancelled in its current status"
                raise InvalidMatchStatus(msg)

            match.status = Status.CANCELLED
            match.save(update_fields=["status", "updated_at"])

            listing = match.listing
            if listing.status == ChequeListing.Status.MATCHED:
                listing.status = ChequeListing.Status.PUBLISHED
                listing.save(update_fields=["status", "updated_at"])

            MatchCancelled.send(sender=Match, match=match, user=user)

            return match

    @staticmethod
    def confirm_off_platform(match_id, user):
        with transaction.atomic():
            match = Match.objects.select_for_update().get(id=match_id)

            if match.check_holder_id != user.id:
                msg = "Only the check holder can confirm settlement"
                raise MatchNotAllowed(msg)

            if match.status != Status.ACCEPTED:
                msg = "Match must be accepted to confirm settlement"
                raise InvalidMatchStatus(msg)

            match.status = Status.OFF_PLATFORM_CONFIRMED
            match.save(update_fields=["status", "updated_at"])

            OffPlatformSettlement.objects.create(
                match=match,
                confirmation_code="",
                confirmed_by=user,
                confirmed_at=timezone.now(),
            )

            SettlementConfirmed.send(sender=Match, match=match, user=user)

            return match
