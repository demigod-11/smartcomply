import os
from pathlib import Path

import environ

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

env = environ.Env(
    DJANGO_ENV=(str, "dev"),
    DEBUG=(bool, False),
    Q_CLUSTER_SYNC=(bool, False),
)

if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)


def resolve_settings_module(django_env: str) -> str:
    match django_env.lower():
        case "dev" | "development":
            return "config.settings.dev"
        case "prod" | "production":
            return "config.settings.prod"
        case "test":
            return "config.settings.test"
        case _:
            raise ValueError(
                f"Unknown DJANGO_ENV={django_env!r}. "
                "Expected one of: dev, prod, test."
            )


def setup_django_settings_module() -> str:
    """Load .env, map DJANGO_ENV to settings module, and set DJANGO_SETTINGS_MODULE."""
    django_env = env("DJANGO_ENV")
    settings_module = resolve_settings_module(django_env)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    return settings_module
