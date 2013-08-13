### Base Settings

import os

##############
### Path Stuff
##############

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
REPO_PATH = os.path.dirname(PROJECT_PATH)

rel = lambda *args: os.path.abspath(os.path.join(REPO_PATH, *args))

####################
### General Settings
####################

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('Dan Sackett', 'danesackett@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['*']
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

ROOT_URLCONF = 'mydash.urls'

WSGI_APPLICATION = 'mydash.wsgi.application'

SECRET_KEY = ''


########
### Apps
########

INSTALLED_APPS = (
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Libs
    'south',
    # My apps
    'account',
    'auth',
    'bookmarks',
    'tags',
    'reminders',
    'notes',
    'todolists',
)


##############
### Middleware
##############

MIDDLEWARE_CLASSES = (
    # defaults
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # custom
    'mydash.middleware.require_login',
)


#############
### Databases
#############


###########
### Logging
###########

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#############
### Templates
#############

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    rel('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # defaults
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    # custom
    'mydash.context_processors.global_values',
)


##################
### Media / Static
##################

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = rel('public')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    rel('public'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


#####################
### Email Information
#####################

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'bookmarks_sackettsolutions'
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'noreply@sackettsolutions.com'
SERVER_EMAIL = 'noreply@sackettsolutions.com'
