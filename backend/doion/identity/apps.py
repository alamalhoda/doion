from django.apps import AppConfig


class IdentityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doion.identity"
    verbose_name = "Identity"

    def ready(self):
        import doion.identity.role_sync  # noqa: F401, PLC0415
