"""Identity factories for tests and demo seeding."""

from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from doion.identity.models import Profile
from doion.identity.models import Verification
from doion.users.factories import UserFactory


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    role = factory.LazyAttribute(lambda o: o.user.role or Profile.Role.CHECK_HOLDER)
    user_type = Profile.UserType.NATURAL
    bio = ""
    is_verified = False

    class Params:
        verified = factory.Trait(is_verified=True)
        legal = factory.Trait(user_type=Profile.UserType.LEGAL)


class VerificationFactory(DjangoModelFactory):
    class Meta:
        model = Verification

    user = factory.SubFactory(UserFactory)
    full_name = factory.LazyAttribute(lambda o: o.user.name or o.user.username)
    national_id = factory.Sequence(lambda n: f"{1000000000 + n}"[:10])
    company_name = ""
    status = Verification.Status.PENDING

    class Params:
        approved = factory.Trait(status=Verification.Status.APPROVED)
        rejected = factory.Trait(
            status=Verification.Status.REJECTED,
            rejection_code="KYC_001",
            rejection_reason="Documents unclear",
        )
        legal = factory.Trait(
            national_id="10100345678",
            company_name="Demo Legal Co",
        )
