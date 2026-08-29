"""Notification factories for tests and demo seeding."""

from __future__ import annotations

import factory
from factory.django import DjangoModelFactory

from doion.notifications.constants import NotificationChannel
from doion.notifications.constants import NotificationStatus
from doion.notifications.constants import NotificationType
from doion.notifications.models import Notification
from doion.notifications.models import NotificationPreference
from doion.users.factories import UserFactory


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(UserFactory)
    type = NotificationType.MATCH_CREATED
    channel = NotificationChannel.IN_APP
    status = NotificationStatus.PENDING
    title = factory.Sequence(lambda n: f"Notification {n}")
    message = factory.LazyAttribute(lambda o: f"Message for {o.title}")
    related_object_type = None
    related_object_id = None

    class Params:
        as_sent = factory.Trait(status=NotificationStatus.SENT)
        as_read = factory.Trait(status=NotificationStatus.READ)


class NotificationPreferenceFactory(DjangoModelFactory):
    class Meta:
        model = NotificationPreference

    user = factory.SubFactory(UserFactory)
    in_app_enabled = True
    sms_enabled = False
    email_enabled = True
