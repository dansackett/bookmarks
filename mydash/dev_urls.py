from django.conf import settings
from django.conf.urls.defaults import patterns

from mydash.urls import *


# handle media urls through django
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
