import logging

from django.db.models.signals import pre_save, post_save, post_migrate
from django.dispatch import receiver

from doion.checks.models import ChequeListing
from doion.compliance.audit import audit_event
from doion.compliance.models import AuditEvent
from doion.compliance.models import FeatureFlag
from doion.identity.models import Profile
from doion.identity.signals import verification_approved
from doion.identity.signals import verification_rejected
from doion.moderation.signals import ChequeListingPublished
from doion.moderation.signals import ListingRejected

logger = logging.getLogger(__name__)


@receiver(ChequeListingPublished)
def on_listing_published(sender, listing, moderator, **kwargs):
    audit_event(
        AuditEvent.EventType.LISTING_PUBLISHED,
        actor=moderator,
        object_type="cheque_listing",
        object_id=str(listing.id),
        request=kwargs.get("request"),
    )


@receiver(ListingRejected)
def on_listing_rejected(
    sender, listing, moderator, rejection_code, rejection_note, **kwargs
):
    audit_event(
        AuditEvent.EventType.LISTING_REJECTED,
        actor=moderator,
        object_type="cheque_listing",
        object_id=str(listing.id),
        metadata={"rejection_code": rejection_code, "rejection_note": rejection_note},
        request=kwargs.get("request"),
    )


@receiver(verification_approved)
def on_verification_approved(sender, verification, **kwargs):
    Profile.objects.filter(user=verification.user).update(is_verified=True)
    audit_event(
        AuditEvent.EventType.KYC_APPROVED,
        actor=None,
        object_type="verification",
        object_id=str(verification.id),
    )


@receiver(verification_rejected)
def on_verification_rejected(
    sender, verification, rejection_code, rejection_note, **kwargs
):
    Profile.objects.filter(user=verification.user).update(is_verified=False)
    audit_event(
        AuditEvent.EventType.KYC_REJECTED,
        actor=None,
        object_type="verification",
        object_id=str(verification.id),
        metadata={"rejection_code": rejection_code, "rejection_note": rejection_note},
    )


@receiver(pre_save, sender=FeatureFlag)
def cache_feature_flag_old_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_is_enabled = sender.objects.get(pk=instance.pk).is_enabled
        except sender.DoesNotExist:
            instance._old_is_enabled = None
    else:
        instance._old_is_enabled = None


@receiver(post_save, sender=FeatureFlag)
def on_feature_flag_changed(sender, instance, created, **kwargs):
    if not created and getattr(instance, "_old_is_enabled", None) is not None:
        if instance._old_is_enabled != instance.is_enabled:
            audit_event(
                AuditEvent.EventType.FEATURE_FLAG_CHANGED,
                object_type="feature_flag",
                object_id=instance.key,
                metadata={
                    "old_value": instance._old_is_enabled,
                    "new_value": instance.is_enabled,
                },
            )


@receiver(post_migrate)
def seed_default_feature_flags(sender, **kwargs):
    if sender.name != "doion.compliance":
        return
    FeatureFlag.objects.get_or_create(
        key="matching_enabled",
        defaults={
            "is_enabled": True,
            "is_system": False,
            "description": "Enable investor express-interest / matching flow",
        },
    )
    FeatureFlag.objects.get_or_create(
        key="notifications_sms_enabled",
        defaults={
            "is_enabled": True,
            "is_system": False,
            "description": "Enable SMS notifications",
        },
    )
    FeatureFlag.objects.get_or_create(
        key="show_risk_tier",
        defaults={
            "is_enabled": False,
            "is_system": False,
            "description": (
                "Show listing risk tier on public marketplace and listing cards. "
                "Moderators always see risk during review."
            ),
        },
    )
    FeatureFlag.objects.get_or_create(
        key="show_landing_page",
        defaults={
            "is_enabled": False,
            "is_system": False,
            "description": (
                "Serve the public landing page at /landing and route / to it. "
                "Off by default until the page is ready to show to guests."
            ),
        },
    )
