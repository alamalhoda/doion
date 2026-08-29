from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "doion.notifications"

    def ready(self):
        import doion.notifications.signals  # noqa: F401, PLC0415
