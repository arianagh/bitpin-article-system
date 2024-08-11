# noinspection PyUnresolvedReferences

from core.settings.base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
HOSTNAME = 'localhost:8000'
USE_SSL = False

ALLOWED_HOSTS = ['*']

MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INSTALLED_APPS.append('debug_toolbar')
