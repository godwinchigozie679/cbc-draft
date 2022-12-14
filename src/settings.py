"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import django_heroku
import dj_database_url
from decouple import config


# Messages
from django.contrib.messages import constants as messages

# Import for email register verification
from account.gft.info import *


# Email Details for register verification
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
# PAGINATION
pagination_number = 8

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!-bgb2ij7o+#fupc!698$n=qvun9jf=ji+kcu^681h8&wvpga-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# if DEBUG:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Development Only
   
# SOcial for PostgresSQL
SOCIAL_AUTH_JSONFIELD_ENABLED = True   
    
ALLOWED_HOSTS = ['*']

# Just added
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'


AUTH_USER_MODEL = "account.Account" 

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'account.backend.CaseInsensitiveModelBackend',
    # Social Auth
    # 'social_core.backends.open_id.OpenIdAuth',
    # 'social_core.backends.google.GoogleOpenId',
    # 'social_core.backends.google.GoogleOAuth2',
    # 'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.twitter.TwitterOAuth',
    # 'social_core.backends.facebook.FacebookOAuth2',
    # 'social_core.backends.yahoo.YahooOpenId',
    # 'django.contrib.auth.backends.ModelBackend',
)

# Application definition

INSTALLED_APPS = [
    # 'whitenoise_runserver_nostatic',
    'blog.apps.BlogConfig',    
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'e_learning.apps.ELearningConfig',
    'payment.apps.PaymentConfig',
    'social_handle.apps.SocialHandleConfig',
    'metafeatures.apps.MetafeaturesConfig',

        
    # 3rd Party
    'active_link',    
    'crispy_forms',
    'taggit',
    'django_social_share',
    'mptt',
    
]

CRISPY_TEMPLATE_PACK = 'uni_form'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
    'e_learning.middleware.AjaxMiddleware',    
    
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'src.wsgi.application'


# Boostrap Messages
MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'ddbshl19t9e2sv',
        # 'USER': 'ftamgogbohtekm',
        # 'PASSWORD': '321337f8f63f990446b00579c995e3213406a540e527c9b33277bb0a13d0a99f',
        # 'HOST': 'ec2-34-234-240-121.compute-1.amazonaws.com',
        # 'PORT': '5432',
        'NAME': 'cbc',
        'USER': 'chigozie',
        'PASSWORD': '123456',
        'HOST': 'localhost', 
    
    
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]



MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = BASE_DIR / "media"



STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
# WHITENOISE_USE_FINDERS = True
# WHITENOISE_MANIFEST_STRICT = False
# WHITENOISE_ALLOW_ALL_ORIGINS = True


CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "/media/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
        'width': 'auto',
    },
}


# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#...
SITE_ID = 1

####################################
    ##  CKEDITOR CONFIGURATION ##
####################################

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

#  PAYSTACK KEYS
PAYSTACK_SECRET_KEY = 'sk_test_91ea127069a2e935c5dd98f51de416fa8a0a80ab'
PAYSTACK_PUBLIC_KEY = 'pk_test_52299579c0d5504d20141c1092f8b3022f085e7c'

# PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
# PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

DEBUG_PROPAGATE_EXCEPTIONS = True

django_heroku.settings(locals())
