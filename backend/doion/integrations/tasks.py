try:
    from celery import shared_task
except ImportError:
    shared_task = None

import logging
from datetime import date

from doion.checks.models import ChequeListing

logger = logging.getLogger(__name__)


def expire_listings():
    """Expire listings with due_date passed and status published."""
    expired_count = 0

    expired_listings = ChequeListing.objects.filter(
        status=ChequeListing.Status.PUBLISHED,
        due_date__lt=date.today(),
    )

    for listing in expired_listings:
        listing.status = ChequeListing.Status.EXPIRED
        listing.save(update_fields=["status", "updated_at"])
        expired_count += 1
        logger.info("Expired listing %s (due_date: %s)", listing.id, listing.due_date)

    logger.info("Expired %d listings", expired_count)
    return {"expired_count": expired_count}


if shared_task is not None:
    expire_listings = shared_task(expire_listings)