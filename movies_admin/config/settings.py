import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from split_settings.tools import include

try:
    # для возможности локального запуска
    load_dotenv(
        dotenv_path=find_dotenv(
            "../../env/.env.movies_admin",
            raise_error_if_not_found=True,
        ),
        verbose=True,
    )

    load_dotenv(
        dotenv_path=find_dotenv(
            "../../env/.env.postgresql",
            raise_error_if_not_found=True,
        ),
        verbose=True,
    )
except IOError:
    pass


include(
    "components/database.py",
    "components/application_definition.py",
    "components/password_validation.py",
    "components/internationalization.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
        },
    },
    "handlers": {
        "debug-console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["require_debug_true"],
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["debug-console"],
            "propagate": False,
        }
    },
}
