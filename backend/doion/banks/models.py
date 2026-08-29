from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from doion.core.models import TimeStampedModel

BRAND_COLOR_REGEX = r"^#[0-9A-Fa-f]{6}$"
brand_color_validator = RegexValidator(
    regex=BRAND_COLOR_REGEX,
    message=_("Brand color must be #RRGGBB."),
)


class Bank(TimeStampedModel):
    code = models.SlugField(max_length=32, unique=True)
    display_name = models.CharField(max_length=100)
    aliases = models.JSONField()
    logo = models.ImageField(upload_to="banks/logos/", null=True, blank=True)
    brand_color_light = models.CharField(
        max_length=7,
        validators=[brand_color_validator],
    )
    brand_color_dark = models.CharField(
        max_length=7,
        validators=[brand_color_validator],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
        ordering = ["display_name"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._original_code = self.code

    def __str__(self) -> str:
        return self.display_name

    def clean(self) -> None:
        super().clean()
        self._validate_aliases()

    def save(self, *args, **kwargs) -> None:
        if not self._state.adding and self.code != self._original_code:
            msg = _("Bank code cannot be changed after creation.")
            raise ValidationError({"code": msg})
        super().save(*args, **kwargs)
        self._original_code = self.code

    def _validate_aliases(self) -> None:
        aliases = self.aliases
        if not isinstance(aliases, list) or not aliases:
            msg = _("aliases must be a non-empty list of strings.")
            raise ValidationError({"aliases": msg})
        if any(not isinstance(item, str) or not item.strip() for item in aliases):
            msg = _("each alias must be a non-empty string.")
            raise ValidationError({"aliases": msg})
        if self.display_name not in aliases:
            msg = _("aliases must include display_name.")
            raise ValidationError({"aliases": msg})
        if len(aliases) != len(set(aliases)):
            msg = _("aliases must be unique within the same bank.")
            raise ValidationError({"aliases": msg})

        others = Bank.objects.all()
        if self.pk:
            others = others.exclude(pk=self.pk)
        for other in others.only("aliases", "code"):
            other_aliases = other.aliases if isinstance(other.aliases, list) else []
            overlap = set(aliases) & set(other_aliases)
            if overlap:
                first = sorted(overlap)[0]
                msg = _("Alias already used by another bank: %(alias)s") % {
                    "alias": first,
                }
                raise ValidationError({"aliases": msg})
