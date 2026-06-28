from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from doion.checks.models import ChequeListing

CACHE_TRIGGER_STATUSES = {
    ChequeListing.Status.PUBLISHED,
    ChequeListing.Status.REJECTED,
    ChequeListing.Status.EXPIRED,
    ChequeListing.Status.WITHDRAWN,
}


def _invalidate_marketplace_cache():
    try:
        cache.delete_pattern("marketplace:listings:*")
    except (AttributeError, NotImplementedError):
        for page in range(1, 51):
            cache.delete(f"marketplace:listings:{page}")


@receiver(post_save, sender=ChequeListing)
def invalidate_marketplace_cache(sender, instance, created, **kwargs):
    if instance.status in CACHE_TRIGGER_STATUSES:
        _invalidate_marketplace_cache()
