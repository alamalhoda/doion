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
from doion.matching.constants import SettlementType
from doion.matching.constants import Status as MatchStatus
from doion.matching.models import Match
from doion.users.models import User

DEMO_USERS = (
    ("holder1", User.Role.CHECK_HOLDER, "CheckHolder"),
    ("investor1", User.Role.INVESTOR, "Investor"),
    ("moderator1", User.Role.MODERATOR, "Moderator"),
    ("admin1", User.Role.ADMIN, "Admin"),
)


class Command(BaseCommand):
    help = (
        "Seed demo users/listings/match using domain factories. "
        "Intended for local/manual and future E2E scenarios. Idempotent by username/serial."
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
            usernames = [username for username, _, _ in DEMO_USERS]
            deleted, _ = User.objects.filter(username__in=usernames).delete()
            self.stdout.write(f"Removed existing demo users ({deleted} related objects).")

        users: dict[str, User] = {}
        for username, role, group_name in DEMO_USERS:
            defaults = {
                "role": role,
                "email": f"{username}@demo.chequeyar.local",
                "name": username,
                "is_staff": role in {User.Role.MODERATOR, User.Role.ADMIN},
                "is_superuser": role == User.Role.ADMIN,
            }
            user, created = User.objects.get_or_create(username=username, defaults=defaults)
            if not created:
                for field, value in defaults.items():
                    setattr(user, field, value)
            user.set_password(password)
            user.save()

            Profile.objects.update_or_create(
                user=user,
                defaults={"role": role, "is_verified": True, "bio": ""},
            )
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            users[username] = user
            action = "created" if created else "updated"
            self.stdout.write(f"  {action}: {username} ({role})")

        holder = users["holder1"]
        investor = users["investor1"]

        issuer, _ = IssuerProfile.objects.get_or_create(
            national_or_company_id="1000000001",
            defaults={"name": "Demo Issuer Co", "credit_score": 720},
        )

        due = timezone.now().date() + timedelta(days=60)
        listing_specs = (
            ("1000000000000001", "بانک ملت", ChequeListing.Status.PENDING_MODERATION),
            ("1000000000000002", "بانک ملی", ChequeListing.Status.PUBLISHED),
            ("1000000000000003", "بانک صادرات", ChequeListing.Status.REJECTED),
        )
        listings: dict[str, ChequeListing] = {}
        for serial, bank_name, status in listing_specs:
            listing, _ = ChequeListing.objects.update_or_create(
                issuer=issuer,
                bank_name=bank_name,
                cheque_serial_number=serial,
                defaults={
                    "owner": holder,
                    "face_amount": Decimal("500000000"),
                    "due_date": due,
                    "issuer_type": ChequeListing.IssuerType.LEGAL,
                    "issuer_name": issuer.name,
                    "issuer_national_id": issuer.national_or_company_id,
                    "description": "Demo listing",
                    "suggested_discount_rate": Decimal("5.00"),
                    "risk_tier": "medium",
                    "status": status,
                    "rejection_code": "MOD_101" if status == ChequeListing.Status.REJECTED else None,
                    "rejection_reason": (
                        "Demo rejection" if status == ChequeListing.Status.REJECTED else ""
                    ),
                },
            )
            listings[serial] = listing

        published = listings["1000000000000002"]
        match, _ = Match.objects.update_or_create(
            listing=published,
            investor=investor,
            defaults={
                "check_holder": holder,
                "status": MatchStatus.PENDING,
                "settlement_type": SettlementType.OFF_PLATFORM,
                "message": "Demo interest",
                "terms": "",
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo seed complete."))
        self.stdout.write(f"Password for all demo users: {password}")
        self.stdout.write(
            "Users: holder1, investor1, moderator1, admin1 "
            f"| listings: pending={listings['1000000000000001'].id}, "
            f"published={published.id}, rejected={listings['1000000000000003'].id} "
            f"| match={match.id}"
        )
