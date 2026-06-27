from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.core.models import TimeStampedModel


class Profile(TimeStampedModel):
    class Role(models.TextChoices):
        CHECK_HOLDER = "check_holder", _("Check Holder")
        INVESTOR = "investor", _("Investor")
        MODERATOR = "moderator", _("Moderator")
        ADMIN = "admin", _("Admin")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        _("Role"),
        max_length=20,
        choices=Role.choices,
        default=Role.CHECK_HOLDER,
    )
    bio = models.TextField(blank=True, default="")
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.username} ({self.role})"
