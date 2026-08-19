"""User factories for tests and demo seeding."""

from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from doion.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    role = User.Role.CHECK_HOLDER
    name = factory.LazyAttribute(lambda o: o.username)

    @factory.post_generation
    def password(self, create: bool, extracted: str | None, **kwargs) -> None:  # noqa: FBT001
        raw_password = extracted if extracted is not None else "testpass123"
        self.set_password(raw_password)
        if create:
            self.save(update_fields=["password"])

    class Params:
        as_investor = factory.Trait(role=User.Role.INVESTOR)
        as_moderator = factory.Trait(role=User.Role.MODERATOR, is_staff=True)
        as_admin = factory.Trait(role=User.Role.ADMIN, is_staff=True, is_superuser=True)
