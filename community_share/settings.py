"""
Django settings for community_share project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2!2s(p*82t61l7@901s%5!)^m_slkv^9#*hse1y)50zs*rx52+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'share.apps.ShareConfig',
    'django.contrib.admin',
    'django.contrib.auth', #Core authentication framework and its default models.
    'django.contrib.contenttypes', #Django content type system (allows permissions to be associated with models).
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', #Manages sessions across requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', #Associates users with requests using sessions.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'community_share.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'community_share.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Redirect to summary.html after login (Default redirects to /accounts/profile/)
# LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/share/summary'
LOGOUT_REDIRECT_URL = '/share/logged_out.html'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# from https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #for debugging
else:
    EMAIL_HOST = 'smtp.mail.yahoo.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'your sending address'
    EMAIL_HOST_PASSWORD = 'your password' #Use environment variable instead
    #EMAIL_USE_TLS = True
    EMAIL_USE_SSL = True
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #for debugging
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # for production

# Server Address: smtp.mail.yahoo.com.
# Username: Your Yahoo Address (e.g. example@yahoo.com)
# Password: Your Yahoo Password.
# Port Number: 465 (With SSL)
# Alternative Port Number: 587 (With TLS)
# Authentication: Required.
