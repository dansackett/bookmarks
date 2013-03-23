from django.conf import settings
from django.conf.urls import patterns, include
from django.shortcuts import redirect


urlpatterns = patterns('',
    (r'^$', lambda r: redirect('login')),
    (r'^', include('auth.urls')),
    (r'^account/', include('account.urls')),
)

if settings.DEBUG:
    # enable admin
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        (r'^admin/', include(admin.site.urls)),
    )

    # handle media urls through django
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
