from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('reminders.views',
    (r'^$', 'list_reminders', {}, 'list-reminders'),
    (r'^add/$', 'add_reminder', {}, 'add-reminder'),
    (r'^edit/(?P<slug>[\w-]+)/$', 'edit_reminder', {}, 'edit-reminder'),
    (r'^delete/(?P<slug>[\w-]+)/$', 'delete_reminder', {}, 'delete-reminder'),
    (r'^view/(?P<slug>[\w-]+)/$', 'view_reminder', {}, 'view-reminder'),
    (r'^dismiss/(?P<slug>[\w-]+)/$', 'dismiss_reminder', {}, 'dismiss-reminder'),
)
