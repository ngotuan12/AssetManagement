"""
Django settings for AssetWebapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%x_9v7!okuyntl14^1mjvq=*&hyn!fn&8oplwb0manp*8=#b-z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*', ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AdminManagement',
    'myapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
#     'myapp.util.middleware.LastActivityMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)
ROOT_URLCONF = 'AssetWebapp.urls'

WSGI_APPLICATION = 'AssetWebapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'db',
        'USER': 'ASSET',
        'PASSWORD': 'asset',
        'HOST': '10.0.3.10',
        'PORT': '1521',
    },
    'default_1': {
        'ENGINE': 'oraclepool',
        'NAME': 'db',
        'USER': 'ASSET',
        'PASSWORD': 'asset',
        'HOST': 'localhost',
        'PORT': '1521',
        'EXTRAS': {'min':1,  # start number of connections
                    'max':20,  # max number of connections
                    'increment':2,  # increase by this amount when more are needed
                    'homogeneous':1,  # 1 = single credentials, 0 = multiple credentials
                    'threaded':True,  # server platform optimisation 
                    'timeout':10,  # connection timeout, 600 = 10 mins
                    'log':0,  # extra logging functionality
                    'logpath':os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/log",  # file system path to log file
                    'existing':'Unicode',  # Type modifications if using existing database data
                    'session': ["alter session set session_cached_cursors = 8;",
                                "alter session set cursor_sharing = 'SIMILAR'"]
                   },
        'OPTIONS': {
                        'autocommit': True,
                    }
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False
LOCALE_PATHS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/locale", # replace with correct path here
)
LANGUAGES = (
    ('en', 'English'),
    ('vi', 'VietNamese'),
    ('de', 'Germany'),
    ('ja','Japanese')
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

LOGIN_REDIRECT_URL = '/home/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/common"
REPORT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/report"
LOG_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/log"
UPLOAD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/upload"
TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
                os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/templates",
                #os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), '/templates'),
)

REPORT_SERVER = 'http://localhost:8080/AssetServer/'
REPORT_SERVICE = 'ReportService'
PERMISSION_SERVICE = 'AuthorizationService'
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)
if not os.path.exists(REPORT_ROOT):
    os.makedirs(REPORT_ROOT)
if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)
if not os.path.exists(UPLOAD_ROOT):
    os.makedirs(UPLOAD_ROOT)