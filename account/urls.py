from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('account.views',
    (r'^$', 'dashboard', {}, 'user-home'),
)
