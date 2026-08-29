from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for doion.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    class Role(models.TextChoices):
        CHECK_HOLDER = "check_holder", _("Check Holder")
        INVESTOR = "investor", _("Investor")
        MODERATOR = "moderator", _("Moderator")
        ADMIN = "admin", _("Admin")

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    phone = CharField(_("Phone Number"), blank=True, max_length=20, null=True)  # noqa: DJ001
    role = CharField(
        _("Role"),
        max_length=20,
        choices=Role.choices,
        default=Role.CHECK_HOLDER,
        blank=True,
    )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
