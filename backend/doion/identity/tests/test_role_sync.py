"""User.role and Profile.role stay aligned when either side is saved."""

import pytest
from django.contrib.admin.sites import AdminSite
from django.utils.crypto import get_random_string

from doion.identity.factories import ProfileFactory
from doion.identity.models import Profile
from doion.users.admin import UserAdmin
from doion.users.factories import UserFactory
from doion.users.models import User


@pytest.mark.django_db
class TestRoleSync:
    def test_saving_profile_role_updates_user_role(self):
        user = UserFactory.create(
            password=get_random_string(12),
            role=User.Role.CHECK_HOLDER,
        )
        profile = ProfileFactory.create(user=user, role=Profile.Role.CHECK_HOLDER)

        profile.role = Profile.Role.ADMIN
        profile.save()

        user.refresh_from_db()
        assert user.role == User.Role.ADMIN

    def test_saving_user_role_updates_existing_profile(self):
        user = UserFactory.create(
            password=get_random_string(12),
            role=User.Role.CHECK_HOLDER,
        )
        ProfileFactory.create(user=user, role=Profile.Role.CHECK_HOLDER)

        user.role = User.Role.MODERATOR
        user.save()

        user.profile.refresh_from_db()
        assert user.profile.role == Profile.Role.MODERATOR

    def test_user_admin_includes_role_field(self):
        field_names = []
        for _name, opts in UserAdmin(User, AdminSite()).fieldsets:
            field_names.extend(opts["fields"])
        assert "role" in field_names
        assert "role" in UserAdmin(User, AdminSite()).list_display
