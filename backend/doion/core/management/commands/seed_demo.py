"""Seed local demo users and domain objects via shared factories."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string

from doion.checks.models import ChequeListing
from doion.checks.models import IssuerProfile
from doion.identity.models import Profile
from doion.identity.models import Verification
from doion.matching.constants import SettlementType
from doion.matching.constants import Status as MatchStatus
from doion.matching.models import Match
from doion.notifications.constants import NotificationChannel
from doion.notifications.constants import NotificationStatus
from doion.notifications.constants import NotificationType
from doion.notifications.models import Notification
from doion.notifications.models import NotificationPreference
from doion.users.models import User

DEMO_USERS = (
    # username, role, group_name, user_type
    ("holder1", User.Role.CHECK_HOLDER, "CheckHolder", Profile.UserType.NATURAL),
    ("investor1", User.Role.INVESTOR, "Investor", Profile.UserType.NATURAL),
    ("moderator1", User.Role.MODERATOR, "Moderator", Profile.UserType.NATURAL),
    ("admin1", User.Role.ADMIN, "Admin", Profile.UserType.NATURAL),
    ("holderkyc1", User.Role.CHECK_HOLDER, "CheckHolder", Profile.UserType.NATURAL),
    ("holderkyclegal1", User.Role.CHECK_HOLDER, "CheckHolder", Profile.UserType.LEGAL),
    ("holderlegal1", User.Role.CHECK_HOLDER, "CheckHolder", Profile.UserType.LEGAL),
    ("investorlegal1", User.Role.INVESTOR, "Investor", Profile.UserType.LEGAL),
)

# Stable serials for E2E critical-path fixtures (16-digit sayad-style).
PUBLISHED_COUNT = 22
PENDING_COUNT = 12
NOTIFICATION_COUNT = 12
ACCEPT_MATCH_SERIAL = "2000000000000001"
DECLINE_MATCH_SERIAL = "2000000000000002"
EXPRESS_INTEREST_SERIAL = "2000000000000022"
REJECT_PENDING_SERIAL = "3000000000000012"
REJECTED_SERIAL = "4000000000000001"

BANKS = (
    "بانک ملت",
    "بانک ملی",
    "بانک صادرات",
    "بانک پاسارگاد",
    "بانک تجارت",
)


class Command(BaseCommand):
    help = (
        "Seed demo users/listings/match/notifications using domain models. "
        "Intended for local/manual and E2E. Idempotent by username/serial."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default=None,
            help="Password for all demo users (random if omitted).",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete previously seeded demo users (by username) before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        password = options["password"] or get_random_string(12)

        if options["reset"]:
            usernames = [username for username, _, _, _ in DEMO_USERS]
            deleted, _ = User.objects.filter(username__in=usernames).delete()
            self.stdout.write(f"Removed existing demo users ({deleted} related objects).")

        users: dict[str, User] = {}
        for username, role, group_name, user_type in DEMO_USERS:
            display_name = {
                "holderlegal1": "Demo Legal Holdings Co",
                "holderkyclegal1": "Pending Legal Co",
                "investorlegal1": "Demo Legal Investor Fund",
            }.get(username, username)
            defaults = {
                "role": role,
                "email": f"{username}@demo.chequeyar.local",
                "name": display_name,
                "is_staff": role in {User.Role.MODERATOR, User.Role.ADMIN},
                "is_superuser": role == User.Role.ADMIN,
            }
            user, created = User.objects.get_or_create(username=username, defaults=defaults)
            if not created:
                for field, value in defaults.items():
                    setattr(user, field, value)
            user.set_password(password)
            user.save()

            is_kyc_pending = username in {"holderkyc1", "holderkyclegal1"}
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "role": role,
                    "user_type": user_type,
                    "is_verified": not is_kyc_pending,
                    "bio": "",
                },
            )
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            users[username] = user
            action = "created" if created else "updated"
            self.stdout.write(f"  {action}: {username} ({role}, {user_type})")

            if username == "holderkyc1":
                Verification.objects.filter(
                    user=user,
                    status=Verification.Status.APPROVED,
                ).delete()
                Verification.objects.get_or_create(
                    user=user,
                    status=Verification.Status.PENDING,
                    defaults={
                        "full_name": "KYC Pending Natural Holder",
                        "national_id": "0012345678",
                        "company_name": "",
                        "rejection_reason": "",
                        "rejection_code": "",
                    },
                )
            elif username == "holderkyclegal1":
                Verification.objects.filter(
                    user=user,
                    status=Verification.Status.APPROVED,
                ).delete()
                Verification.objects.get_or_create(
                    user=user,
                    status=Verification.Status.PENDING,
                    defaults={
                        "full_name": "Pending Legal Representative",
                        "national_id": "10100987654",
                        "company_name": "Pending Legal Co",
                        "rejection_reason": "",
                        "rejection_code": "",
                    },
                )
            elif username in {"holderlegal1", "investorlegal1"}:
                Verification.objects.get_or_create(
                    user=user,
                    status=Verification.Status.APPROVED,
                    defaults={
                        "full_name": "Legal Representative",
                        "national_id": "10100345678" if username == "holderlegal1" else "10100112233",
                        "company_name": display_name,
                        "rejection_reason": "",
                        "rejection_code": "",
                    },
                )
            elif role in {User.Role.CHECK_HOLDER, User.Role.INVESTOR}:
                Verification.objects.get_or_create(
                    user=user,
                    status=Verification.Status.APPROVED,
                    defaults={
                        "full_name": user.name or username,
                        "national_id": f"{1000000000 + user.id}"[:10],
                        "company_name": "",
                        "rejection_reason": "",
                        "rejection_code": "",
                    },
                )

        holder = users["holder1"]
        investor = users["investor1"]

        issuer, _ = IssuerProfile.objects.get_or_create(
            national_or_company_id="1000000001",
            defaults={
                "name": "Demo Issuer Co",
                "credit_score": 720,
                "created_by": holder,
            },
        )
        if issuer.created_by_id is None:
            issuer.created_by = holder
            issuer.save(update_fields=["created_by", "updated_at"])

        due = timezone.now().date() + timedelta(days=60)
        published: dict[str, ChequeListing] = {}
        pending: dict[str, ChequeListing] = {}

        for index in range(1, PUBLISHED_COUNT + 1):
            serial = f"2000000000000{index:03d}"
            listing = self._upsert_listing(
                issuer=issuer,
                owner=holder,
                serial=serial,
                bank_name=BANKS[(index - 1) % len(BANKS)],
                status=ChequeListing.Status.PUBLISHED,
                due=due,
                description=f"Demo published listing {index}",
            )
            published[serial] = listing

        for index in range(1, PENDING_COUNT + 1):
            serial = f"3000000000000{index:03d}"
            listing = self._upsert_listing(
                issuer=issuer,
                owner=holder,
                serial=serial,
                bank_name=BANKS[(index - 1) % len(BANKS)],
                status=ChequeListing.Status.PENDING_MODERATION,
                due=due,
                description=f"Demo pending listing {index}",
            )
            pending[serial] = listing

        rejected = self._upsert_listing(
            issuer=issuer,
            owner=holder,
            serial=REJECTED_SERIAL,
            bank_name="بانک صادرات",
            status=ChequeListing.Status.REJECTED,
            due=due,
            description="Demo rejected listing",
            rejection_code="MOD_101",
            rejection_reason="Demo rejection",
        )

        accept_listing = published[ACCEPT_MATCH_SERIAL]
        match, _ = Match.objects.update_or_create(
            listing=accept_listing,
            investor=investor,
            defaults={
                "check_holder": holder,
                "status": MatchStatus.PENDING,
                "settlement_type": SettlementType.OFF_PLATFORM,
                "message": "Demo interest for accept-match E2E",
                "terms": "",
            },
        )

        decline_listing = published[DECLINE_MATCH_SERIAL]
        decline_match, _ = Match.objects.update_or_create(
            listing=decline_listing,
            investor=investor,
            defaults={
                "check_holder": holder,
                "status": MatchStatus.PENDING,
                "settlement_type": SettlementType.OFF_PLATFORM,
                "message": "Demo interest for decline-match E2E",
                "terms": "",
            },
        )

        NotificationPreference.objects.get_or_create(user=holder)
        for index in range(1, NOTIFICATION_COUNT + 1):
            notif_type = (
                NotificationType.LISTING_PUBLISHED
                if index % 2 == 1
                else NotificationType.MATCH_CREATED
            )
            title = f"Demo notification {index}"
            Notification.objects.update_or_create(
                user=holder,
                title=title,
                channel=NotificationChannel.IN_APP,
                defaults={
                    "type": notif_type,
                    "status": NotificationStatus.SENT,
                    "message": f"Seeded unread notification #{index} for E2E",
                    "related_object_type": "cheque_listing",
                    "related_object_id": str(accept_listing.id),
                    "read_at": None,
                    "sent_at": timezone.now(),
                },
            )

        # Backdate seeded listings so the 10/day create cap remains usable for E2E.
        seeded_ids = (
            list(published.values())
            + list(pending.values())
            + [rejected]
        )
        ChequeListing.objects.filter(id__in=[listing.id for listing in seeded_ids]).update(
            created_at=timezone.now() - timedelta(days=2),
        )

        self.stdout.write(self.style.SUCCESS("Demo seed complete."))
        self.stdout.write(f"Password for all demo users: {password}")
        self.stdout.write(
            "Users: holder1, investor1, moderator1, admin1, holderkyc1 "
            f"| published={PUBLISHED_COUNT} (express={EXPRESS_INTEREST_SERIAL}, "
            f"accept_match={ACCEPT_MATCH_SERIAL}, decline_match={DECLINE_MATCH_SERIAL}) "
            f"| pending={PENDING_COUNT} (reject={REJECT_PENDING_SERIAL}) "
            f"| rejected={rejected.id} "
            f"| match={match.id}/{decline_match.id} "
            f"| notifications={NOTIFICATION_COUNT}"
        )

    def _upsert_listing(
        self,
        *,
        issuer: IssuerProfile,
        owner: User,
        serial: str,
        bank_name: str,
        status: str,
        due,
        description: str,
        rejection_code: str | None = None,
        rejection_reason: str = "",
    ) -> ChequeListing:
        listing, _ = ChequeListing.objects.update_or_create(
            issuer=issuer,
            bank_name=bank_name,
            cheque_serial_number=serial,
            defaults={
                "owner": owner,
                "face_amount": Decimal("500000000"),
                "due_date": due,
                "issuer_type": ChequeListing.IssuerType.LEGAL,
                "issuer_name": issuer.name,
                "issuer_national_id": issuer.national_or_company_id,
                "description": description,
                "suggested_discount_rate": Decimal("5.00"),
                "risk_tier": "medium",
                "status": status,
                "rejection_code": rejection_code,
                "rejection_reason": rejection_reason,
            },
        )
        return listing
