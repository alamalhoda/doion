"""Keep User.role and Profile.role aligned (login/SPA vs Identity admin)."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from doion.identity.models import Profile
from doion.users.models import User


@receiver(post_save, sender=Profile)
def copy_profile_role_to_user(sender, instance, **kwargs):
    User.objects.filter(pk=instance.user_id).exclude(role=instance.role).update(role=instance.role)


@receiver(post_save, sender=User)
def copy_user_role_to_profile(sender, instance, **kwargs):
    Profile.objects.filter(user_id=instance.pk).exclude(role=instance.role).update(role=instance.role)
