import os
import sys

from django.core.handlers.wsgi import WSGIHandler

PROJECT_NAME = 'bookshelf'
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(REPO_DIR, PROJECT_NAME)
APPS_DIR = os.path.join(REPO_DIR, 'apps')
SETTINGS_MODULE = '.'.join((PROJECT_NAME, 'settings'))

sys.path.append(REPO_DIR)  # project
sys.path.append(APPS_DIR)  # local apps

os.environ['DJANGO_SETTINGS_MODULE'] = 'bookshelf.settings'
application = WSGIHandler()
