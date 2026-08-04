"""Tests for seed_demo management command."""

import pytest
from django.core.management import call_command
from django.utils.crypto import get_random_string

from doion.checks.models import ChequeListing
from doion.core.management.commands.seed_demo import ACCEPT_MATCH_SERIAL
from doion.matching.models import Match
from doion.users.models import User


@pytest.mark.django_db
class TestSeedDemoCommand:
    def test_seed_demo_creates_roles_listings_and_match(self, capsys):
        password = get_random_string(12)

        call_command("seed_demo", password=password)

        assert User.objects.filter(username="holder1", role=User.Role.CHECK_HOLDER).exists()
        assert User.objects.filter(username="investor1", role=User.Role.INVESTOR).exists()
        assert User.objects.filter(username="moderator1", role=User.Role.MODERATOR).exists()
        assert User.objects.filter(username="admin1", role=User.Role.ADMIN).exists()

        holder = User.objects.get(username="holder1")
        assert holder.check_password(password)
        assert holder.profile.is_verified is True

        statuses = set(
            ChequeListing.objects.filter(owner=holder).values_list("status", flat=True)
        )
        assert ChequeListing.Status.PENDING_MODERATION in statuses
        assert ChequeListing.Status.PUBLISHED in statuses
        assert ChequeListing.Status.REJECTED in statuses
        assert Match.objects.filter(investor__username="investor1").exists()

        captured = capsys.readouterr()
        assert password in captured.out

    def test_seed_demo_is_idempotent(self):
        password = get_random_string(12)
        call_command("seed_demo", password=password)
        call_command("seed_demo", password=password)

        assert User.objects.filter(username="holder1").count() == 1
        assert ChequeListing.objects.filter(cheque_serial_number=ACCEPT_MATCH_SERIAL).count() == 1
        assert Match.objects.filter(investor__username="investor1").count() == 1
