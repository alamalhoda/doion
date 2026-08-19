from django.utils.translation import gettext_lazy as _


class NotificationType:
    MATCH_CREATED = "match_created"
    MATCH_ACCEPTED = "match_accepted"
    MATCH_DECLINED = "match_declined"
    MATCH_CANCELLED = "match_cancelled"
    SETTLEMENT_CONFIRMED = "settlement_confirmed"
    LISTING_PUBLISHED = "listing_published"
    LISTING_REJECTED = "listing_rejected"
    LISTING_EXPIRED = "listing_expired"
    KYC_APPROVED = "kyc_approved"
    KYC_REJECTED = "kyc_rejected"
    NEW_MODERATION_ITEM = "new_moderation_item"

    CHOICES = [
        (MATCH_CREATED, _("Match Created")),
        (MATCH_ACCEPTED, _("Match Accepted")),
        (MATCH_DECLINED, _("Match Declined")),
        (MATCH_CANCELLED, _("Match Cancelled")),
        (SETTLEMENT_CONFIRMED, _("Settlement Confirmed")),
        (LISTING_PUBLISHED, _("Listing Published")),
        (LISTING_REJECTED, _("Listing Rejected")),
        (LISTING_EXPIRED, _("Listing Expired")),
        (KYC_APPROVED, _("KYC Approved")),
        (KYC_REJECTED, _("KYC Rejected")),
        (NEW_MODERATION_ITEM, _("New Moderation Item")),
    ]


class NotificationChannel:
    IN_APP = "in_app"
    SMS = "sms"
    EMAIL = "email"

    CHOICES = [
        (IN_APP, _("In App")),
        (SMS, _("SMS")),
        (EMAIL, _("Email")),
    ]


class NotificationStatus:
    PENDING = "pending"
    SENT = "sent"
    READ = "read"
    FAILED = "failed"

    CHOICES = [
        (PENDING, _("Pending")),
        (SENT, _("Sent")),
        (READ, _("Read")),
        (FAILED, _("Failed")),
    ]
