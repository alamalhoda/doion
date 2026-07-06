import logging
from typing import Any

from django.dispatch import receiver
from django.utils import timezone

from doion.checks.models import ChequeListing
from doion.integrations.services import send_sms
from doion.moderation.signals import ChequeListingPublished
from doion.moderation.signals import ListingRejected
from doion.notifications.constants import NotificationChannel
from doion.notifications.constants import NotificationStatus
from doion.notifications.constants import NotificationType
from doion.notifications.models import Notification
from doion.notifications.models import NotificationPreference

logger = logging.getLogger(__name__)


def create_notification(
    user,
    notification_type: str,
    title: str,
    message: str,
    related_object_type: str = None,
    related_object_id: str = None,
) -> Notification:
    """Create a notification for a user."""
    preference, _ = NotificationPreference.objects.get_or_create(user=user)

    channels = [NotificationChannel.IN_APP]
    if notification_type in [
        NotificationType.MATCH_CREATED,
        NotificationType.LISTING_PUBLISHED,
    ]:
        if preference.sms_enabled:
            channels.append(NotificationChannel.SMS)

    for channel in channels:
        Notification.objects.create(
            user=user,
            type=notification_type,
            channel=channel,
            status=NotificationStatus.SENT,
            title=title,
            message=message,
            related_object_type=related_object_type,
            related_object_id=related_object_id,
            sent_at=timezone.now() if hasattr(timezone, 'now') else None,
        )

    return Notification.objects.filter(user=user).first()


@receiver(ChequeListingPublished)
def on_listing_published(sender, listing: ChequeListing, moderator, **kwargs):
    logger.info("Listing %s published, creating notification for owner", listing.id)
    create_notification(
        user=listing.owner,
        notification_type=NotificationType.LISTING_PUBLISHED,
        title="آگهی چک تأیید شد",
        message="آگهی چک شما پس از بررسی ناظر تأیید و منتشر شد",
        related_object_type="cheque_listing",
        related_object_id=str(listing.id),
    )


@receiver(ListingRejected)
def on_listing_rejected(
    sender, listing: ChequeListing, moderator, rejection_code, rejection_note, **kwargs
):
    logger.info("Listing %s rejected, creating notification for owner", listing.id)
    create_notification(
        user=listing.owner,
        notification_type=NotificationType.LISTING_REJECTED,
        title="آگهی چک رد شد",
        message=f"آگهی چک شما رد شد. دلیل: {rejection_note}",
        related_object_type="cheque_listing",
        related_object_id=str(listing.id),
    )


# Signal handlers for match events
def handle_match_created(listing: ChequeListing, investor):
    """Create notification for holder when match is created."""
    logger.info("Match created for listing %s, notifying holder", listing.id)
    create_notification(
        user=listing.owner,
        notification_type=NotificationType.MATCH_CREATED,
        title="درخواست خرید جدید",
        message="یک سرمایه‌گذار به آگهی چک شما علاقه‌مند شده است",
        related_object_type="cheque_listing",
        related_object_id=str(listing.id),
    )


def handle_match_accepted(listing: ChequeListing, investor):
    """Create notification for investor when match is accepted."""
    logger.info("Match accepted for listing %s, notifying investor", listing.id)
    create_notification(
        user=investor,
        notification_type=NotificationType.MATCH_ACCEPTED,
        title="درخواست شما پذیرفته شد",
        message="دارنده چک درخواست خرید شما را پذیرفته است",
        related_object_type="cheque_listing",
        related_object_id=str(listing.id),
    )


def handle_match_declined(listing: ChequeListing, investor):
    """Create notification for investor when match is declined."""
    logger.info("Match declined for listing %s, notifying investor", listing.id)
    create_notification(
        user=investor,
        notification_type=NotificationType.MATCH_DECLINED,
        title="درخواست شما رد شد",
        message="دارنده چک درخواست خرید شما را رد کرده است",
        related_object_type="cheque_listing",
        related_object_id=str(listing.id),
    )


def handle_match_cancelled(listing: ChequeListing, investor):
    """Create notification for both parties when match is cancelled."""
    logger.info("Match cancelled for listing %s", listing.id)
    for user in [listing.owner, investor]:
        create_notification(
            user=user,
            notification_type=NotificationType.MATCH_CANCELLED,
            title="تطابق لغو شد",
            message="یکی از طرفین تطابق را لغو کرده است",
            related_object_type="cheque_listing",
            related_object_id=str(listing.id),
        )


def handle_settlement_confirmed(listing: ChequeListing, investor):
    """Create notification for both parties when settlement is confirmed."""
    logger.info("Settlement confirmed for listing %s", listing.id)
    for user in [listing.owner, investor]:
        create_notification(
            user=user,
            notification_type=NotificationType.SETTLEMENT_CONFIRMED,
            title="تسویه تأیید شد",
            message="تسویه‌ی تطابق توسط هر دو طرف تأیید شده است",
            related_object_type="cheque_listing",
            related_object_id=str(listing.id),
        )


# Import timezone for sent_at
from django.utils import timezone  # noqa: E402