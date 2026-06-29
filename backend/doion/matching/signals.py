import logging

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from doion.matching.constants import Status
from doion.matching.models import Match

logger = logging.getLogger(__name__)

MatchCreated = Signal()
MatchAccepted = Signal()
MatchDeclined = Signal()
MatchCancelled = Signal()
SettlementConfirmed = Signal()


@receiver(post_save, sender=Match)
def invalidate_match_cache(sender, instance, created, **kwargs):
    if instance.status in (
        Status.PENDING,
        Status.ACCEPTED,
        Status.DECLINED,
        Status.CANCELLED,
        Status.OFF_PLATFORM_CONFIRMED,
        Status.SETTLED,
    ):
        try:
            cache.delete_pattern("matching:matches:*")
        except (AttributeError, NotImplementedError):
            for page in range(1, 51):
                cache.delete(f"matching:matches:{page}")
