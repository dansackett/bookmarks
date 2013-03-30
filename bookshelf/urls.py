from django.conf import settings
from django.conf.urls import patterns, include
from django.shortcuts import redirect


urlpatterns = patterns('',
    (r'^', include('auth.urls')),
    (r'^account/', include('account.urls')),
    (r'^tags/', include('tags.urls')),
    (r'^bookmarks/', include('bookmarks.urls')),
)

if settings.DEBUG:
    # handle media urls through django
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
