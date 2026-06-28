from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doion.marketplace"

    def ready(self):
        import doion.marketplace.signals  # noqa: F401
