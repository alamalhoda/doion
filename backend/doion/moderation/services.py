from django.db import transaction

from doion.checks.models import ChequeListing
from doion.moderation.constants import MAX_LISTING_RESUBMITS
from doion.moderation.exceptions import ModerationResubmitLimitExceeded
from doion.moderation.models import ModerationDecision
from doion.moderation.signals import ChequeListingPublished
from doion.moderation.signals import ListingRejected


class ModerationService:
    @staticmethod
    def approve_listing(listing_id, moderator):
        with transaction.atomic():
            listing = ChequeListing.objects.select_for_update().get(id=listing_id)

            if listing.status != ChequeListing.Status.PENDING_MODERATION:
                msg = "Listing is not in pending moderation status"
                raise ValueError(msg)

            listing.status = ChequeListing.Status.PUBLISHED
            listing.rejection_reason = ""
            listing.rejection_code = None
            listing.save(
                update_fields=["status", "rejection_reason", "rejection_code", "updated_at"],
            )

            decision = ModerationDecision.objects.create(
                listing=listing,
                moderator=moderator,
                decision=ModerationDecision.Decision.APPROVED,
            )

            ChequeListingPublished.send(
                sender=ChequeListing,
                listing=listing,
                moderator=moderator,
            )

            return decision

    @staticmethod
    def reject_listing(listing_id, moderator, rejection_code, rejection_note):
        with transaction.atomic():
            listing = ChequeListing.objects.select_for_update().get(id=listing_id)

            if listing.status not in (
                ChequeListing.Status.PENDING_MODERATION,
                ChequeListing.Status.REJECTED,
            ):
                msg = "Listing is not in pending moderation status"
                raise ValueError(msg)

            if listing.resubmit_count >= MAX_LISTING_RESUBMITS:
                raise ModerationResubmitLimitExceeded

            if listing.status == ChequeListing.Status.REJECTED:
                listing.resubmit_count += 1
            else:
                listing.resubmit_count = 1

            listing.status = ChequeListing.Status.REJECTED
            listing.rejection_code = rejection_code
            listing.rejection_reason = rejection_note
            listing.save(
                update_fields=[
                    "status",
                    "rejection_code",
                    "rejection_reason",
                    "resubmit_count",
                    "updated_at",
                ],
            )

            decision = ModerationDecision.objects.create(
                listing=listing,
                moderator=moderator,
                decision=ModerationDecision.Decision.REJECTED,
                rejection_code=rejection_code,
                rejection_note=rejection_note,
            )

            ListingRejected.send(
                sender=ChequeListing,
                listing=listing,
                moderator=moderator,
                rejection_code=rejection_code,
                rejection_note=rejection_note,
            )

            return decision
