from django.conf import settings
from django.conf.urls.defaults import patterns

from mydash.urls import *


# handle media urls through django
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

# redirect for favicon
urlpatterns += patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {
        'url': '/media/images/favicon.ico',
    }),
)
