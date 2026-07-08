from django.db import transaction
from django.utils import timezone

from doion.checks.models import ChequeListing
from doion.matching.constants import Status, SettlementType
from doion.matching.exceptions import InvalidMatchStatus, MatchNotAllowed
from doion.matching.models import Match, OffPlatformSettlement
from doion.matching.signals import (
    MatchAccepted,
    MatchCancelled,
    MatchCreated,
    MatchDeclined,
    SettlementConfirmed,
)


class MatchingService:
    @staticmethod
    def create_match(listing_id, investor):
        with transaction.atomic():
            listing = ChequeListing.objects.select_for_update().get(id=listing_id)

            if listing.status != ChequeListing.Status.PUBLISHED:
                raise MatchNotAllowed("Listing is not published")

            if getattr(investor, "role", None) != "investor":
                raise MatchNotAllowed("Only investors can create matches")

            if listing.owner_id == investor.id:
                raise MatchNotAllowed("You cannot match your own listing")

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
                raise InvalidMatchStatus("Match is not pending")

            if match.check_holder_id != check_holder.id:
                raise MatchNotAllowed("You are not authorized to accept this match")

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
                raise InvalidMatchStatus("Match is not pending")

            if match.check_holder_id != check_holder.id:
                raise MatchNotAllowed("You are not authorized to decline this match")

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
                raise MatchNotAllowed("You are not a party to this match")

            if match.status not in (Status.PENDING, Status.ACCEPTED):
                raise InvalidMatchStatus("Match cannot be cancelled in its current status")

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
                raise MatchNotAllowed("Only the check holder can confirm settlement")

            if match.status != Status.ACCEPTED:
                raise InvalidMatchStatus("Match must be accepted to confirm settlement")

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
