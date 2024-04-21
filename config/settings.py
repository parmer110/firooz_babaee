from pathlib import Path
import os
from .logging_setup import LOGGING


VERSION = "1.0.2"

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-$r4i7=qy1up6b+^=a3f7hvdcpk=#4j^ct=%q1buyad!@_vklp!'

DEBUG = True

ALLOWED_HOSTS = ['185.231.115.248','*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'rest_framework',
    'rest_framework.authtoken',
    'maintenancemode', 
    'uploader',
    'order',   
    'barcode',   
    'inquiryHistory',
    'customer',
    'account',
    'products',
    'InspectionDetails',
    'inspections',
    'Shipping',
    'ShippingDetails',
    'Tasks',
    'companies',
    
]

MIDDLEWARE = [
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR.joinpath('Templates'))
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.media', #<-- HEREوعسث هئشلث عحمخشی هد حشلث  صثذسهفث
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'amf_frz_db2',
        'USER': 'djangouser',
        'PASSWORD': 'amf@psql2022',
        'HOST': 'localhost',
        'PORT': '',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = False

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))


LOGIN_REDIRECT_URL='panel'
LIOGOUT_REDIRECT_URL='panel'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL='account.CustomUser'

CRISPY_TEMPLATE_PACK='bootstrap4'

EMAIL_BACKEND='djando.core.mail.backends.console.EmailBakcend'
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
SITE_ROOT = PROJECT_ROOT


MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
#STATICFILES_DIRS = STATICFILES_DIRS = (
#os.path.join('Templates', 'static'),
#y
"/home/firooze/static",
#)
STATIC_URL = '/static/'


# STATICFILES_DIRS = (
# #     # Put strings here, like "/home/html/static" or "C:/www/django/static".
# #     # Always use forward slashes, even on Windows.
#       "C:\Hamgom\firooze\Templates",
#       os.path.join(SITE_ROOT, 'staticfiles'),
# )

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'Templates'),
)
REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': [
'rest_framework.authentication.TokenAuthentication',
]
}
# Enable / disable maintenance mode.
# Default: False
#MAINTENANCE_MODE = True  # or ``False`` and use ``maintenance`` command

# Sequence of URL path regexes to exclude from the maintenance mode.
# Default: ()
#MAINTENANCE_IGNORE_URLS = (
#    r'^/docs/.*',
#    r'^/contact'
#)
CRISPY_TEMPLATE_PACK = 'bootstrap4'