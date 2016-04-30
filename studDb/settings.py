"""
Django settings for studDb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings
from db import DATABASES

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1r5_d4(&4^6g=fn*du*9p_64@6t5+t+y0xm&cxc7y$a4m=&nvj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
    "studDb.context_processors.students_proc",
    "students.context_processors.groups_processor",
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contact_form',
    'crispy_forms',
    'students',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'studDb.urls'

WSGI_APPLICATION = 'studDb.wsgi.application'

PORTAL_URL = 'http://localhost:8000'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# database in file db.py

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'uk-Uk'

TIME_ZONE = 'Europe/Zaporozhye'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

SIZE_LIMIT_FILE = 2 * 1024 * 1024

#email settings
# from psw import password
ADMIN_EMAIL = 'grydinywka@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'grydinywka@gmail.com'
EMAIL_HOST_PASSWORD = password
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
# ADMIN_EMAIL = 'grydinywka@gmail.com'
# EMAIL_HOST = 'smtp.sendgrid.net.'
# EMAIL_PORT = '587'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ""
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

CRISPY_TEMPLATE_PACK = 'bootstrap3'

ADMINS = (
    # ('serg', 'grydinywka@gmail.com'),   # email will be sent to your_email
    ('serg2', 'sergeyi@univ.kiev.ua'),
)

MANAGERS = ADMINS


# logger section
LOG_FILE = os.path.join(BASE_DIR, 'studDb.log')

from django.http import UnreadablePostError
# from .colorius import ColorizingStreamHandler

def skip_unreadable_post(record):
    if record.exc_info:
        exc_type, exc_value = record.exc_info[:2]
        if isinstance(exc_value, UnreadablePostError):
            return False
    return False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'filters': {
        'skip_unreadable_posts': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_unreadable_post,
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'studDb.custom_handlers.ColorizingStreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['skip_unreadable_posts'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
        },
        'database': {
            'level': 'DEBUG',
            'class': 'studDb.custom_handlers.DatabaseHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'students.signals': {
            'handlers': ['console', 'file', 'database'],
            'level': 'DEBUG',
        },
        'students.views.contact_admin2': {
            'handlers': ['console', 'file', 'mail_admins', 'database'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR'
        }
    }
}