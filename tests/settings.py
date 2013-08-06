# Django settings for testproj project.

import warnings
warnings.filterwarnings(
        'error', r"DateTimeField received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')

import os
import sys

# import source code dir
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))

from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

SECRET_KEY = get_random_string(50, chars)

SITE_ID = 300

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)


#TEST_RUNNER = "django_nose.run_tests"
#here = os.path.abspath(os.path.dirname(__file__))

MANAGERS = ADMINS

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'djpgtrigger_test',
            }
        }

INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'south',
        'djorm_hstore',
        'pgaudit',
        'someapp',
)

USE_TZ = True
TIME_ZONE = 'UTC'
