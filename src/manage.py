#!/usr/bin/env python
import os
import sys

from config.env import setup_django_settings_module


def main():
    setup_django_settings_module()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Is it installed and on your PYTHONPATH?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
