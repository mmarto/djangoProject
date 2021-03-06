"""
Django settings for djangoProject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

REPORTS_DIR = os.path.join(os.environ['HOME'], 'ibcs', 'data', 'reportsViewer')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j3)6)kq4(xt5@v!jf^@2=u=zdp!z^ac2!$=s**t7!cpx1w0)cg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    #'reportsViewer.backends.ImapCustomBackend.ImapCustomBackend',
    'reportsViewer.backends.IBWebCustomBackend.IBWebCustomBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'reportsViewer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangoProject.urls'

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.oracle',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'ibcust.dev2',
        'HOST': '',
        'PORT': '',
        'USER': 'ibreporter',
        'PASSWORD': 'nopassword',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

EMAIL_HOST = 'smail100'

EMAIL_PORT = 25

EMAIL_HOST_USER = 'mhristov'

EMAIL_HOST_PASSWORD = ''
