### Production Settings

from .base import *


##############
### Path Stuff
##############


####################
### General Settings
####################


########
### Apps
########


##############
### Middleware
##############

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


#############
### Databases
#############

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'bookmarks',
        'USER':     'bookmarks_user',
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

STATIC_ROOT = '/home/dansackett/webapps/bookmarks_static/'
STATIC_URL = 'https://mydashapp.com/static/'


#####################
### Email Information
#####################

EMAIL_HOST_PASSWORD = ''
