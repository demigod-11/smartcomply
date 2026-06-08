from django.core.wsgi import get_wsgi_application

from config.env import setup_django_settings_module

setup_django_settings_module()

application = get_wsgi_application()
