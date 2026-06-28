import logging

from django.dispatch import Signal
from django.dispatch import receiver

logger = logging.getLogger(__name__)

ChequeListingPublished = Signal()
ListingRejected = Signal()


@receiver(ChequeListingPublished)
def on_listing_published(sender, listing, moderator, **kwargs):
    logger.info(
        "Listing %s published by moderator %s (placeholder: send notification to owner)",
        listing.id,
        moderator,
    )


@receiver(ListingRejected)
def on_listing_rejected(sender, listing, moderator, rejection_code, rejection_note, **kwargs):
    logger.info(
        "Listing %s rejected by moderator %s (code: %s, note: %s). "
        "Owner notification placeholder — Phase 7 will implement real delivery.",
        listing.id,
        moderator,
        rejection_code,
        rejection_note,
    )
