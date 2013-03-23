from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('auth.views',
    (r'^login/$', 'login', {}, 'login'),
    (r'^logout/$', 'logout', {}, 'logout'),
    (r'^register/$', 'register', {}, 'register'),
)
