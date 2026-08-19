
from django.apps import AppConfig


class ComplianceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doion.compliance"

    def ready(self):
        from django.db.models.signals import post_migrate  # noqa: PLC0415

        from doion.compliance.signals import seed_default_feature_flags  # noqa: PLC0415
        post_migrate.connect(seed_default_feature_flags, sender=self)
        import doion.compliance.signals  # noqa: F401, PLC0415
