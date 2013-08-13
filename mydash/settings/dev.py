### Development Settings

from .base import *


##############
### Path Stuff
##############


####################
### General Settings
####################

DEBUG = True
TEMPLATE_DEBUG = True

ROOT_URLCONF = 'mydash.dev_urls'

# django debug toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
INTERNAL_IPS = ('127.0.0.1',)


########
### Apps
########

INSTALLED_APPS += (
    # Libs
    'django_extensions',
    'debug_toolbar',
)


##############
### Middleware
##############

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


#############
### Databases
#############

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'mydash',
        'USER':     'mydash_user',
        'PASSWORD': '',
        'HOST':     'localhost',
        'PORT':     '',
    }
}


###########
### Logging
###########


#############
### Templates
#############



##################
### Media / Static
##################


#####################
### Email Information
#####################
