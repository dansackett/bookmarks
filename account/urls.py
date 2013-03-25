from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('account.views',
    (r'^$', 'dashboard', {}, 'user-home'),
    (r'^profile/edit/$', 'edit_profile', {}, 'edit-profile'),
)
