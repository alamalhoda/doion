from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BanksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doion.banks"
    verbose_name = "Banks"

    def ready(self) -> None:
        from doion.banks.seed import seed_catalog_banks_on_migrate  # noqa: PLC0415

        post_migrate.connect(seed_catalog_banks_on_migrate, sender=self)
