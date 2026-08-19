"""
With these settings, tests run faster.
"""

import os
from pathlib import Path

from .base import *  # noqa: F403
from .base import TEMPLATES
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="xzH72FQopv0XLCZQVWC9VGvQNkNyxc1efjB57O9YU2Nuvpub47URZYrkJvyVY8iZ",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGGING FOR TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# DATABASES
# ------------------------------------------------------------------------------
# Local pytest: isolated SQLite (does not use config.settings.local / db.sqlite3).
# GitHub Actions: PostgreSQL via DATABASE_URL. No SQLite fallback in CI.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if os.environ.get("GITHUB_ACTIONS"):
    DATABASES = {
        "default": env.db("DATABASE_URL"),
    }
    engine = DATABASES["default"].get("ENGINE", "")
    if "postgres" not in engine:
        msg = "GitHub Actions pytest must use PostgreSQL; SQLite is not allowed."
        raise RuntimeError(msg)
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "test_db.sqlite3",
        },
    }
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Allow sites app to use its default migrations in test environment
MIGRATION_MODULES = {}

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "http://media.testserver/"
# Your stuff...
# ------------------------------------------------------------------------------
