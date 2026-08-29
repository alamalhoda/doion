try:
    from celery import Celery

    app = Celery("doion")
    app.config_from_object("django.conf:settings", namespace="CELERY")
    app.autodiscover_tasks()
except ImportError:
    app = None
