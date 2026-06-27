from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


GROUP_NAMES = ["CheckHolder", "Investor", "Moderator", "Admin"]


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for name in GROUP_NAMES:
        Group.objects.get_or_create(name=name)
