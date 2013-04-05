from django.conf import settings
from django.conf.urls import patterns, include
from django.shortcuts import redirect


urlpatterns = patterns('',
    (r'^$', lambda r: redirect('/login/')),
    (r'^', include('auth.urls')),
    (r'^account/', include('account.urls')),
    (r'^tags/', include('tags.urls')),
    (r'^bookmarks/', include('bookmarks.urls')),
    (r'^reminders/', include('reminders.urls')),
)

if settings.DEBUG:
    # handle media urls through django
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
