from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('reminders.views',
    (r'^$', 'list_reminders', {}, 'list-reminders'),
    (r'^calendar/$', 'reminders_calendar', {}, 'calendar'),
    (r'^calendar/(?P<year>[\d]+)/(?P<month>[\d]+)/$', 'reminders_calendar', {}, 'calendar-date'),
    (r'^calendar/view/(?P<year>[\d]+)/(?P<month>[\d]+)/(?P<day>[\d]+)/$', 'view_day_calendar', {}, 'calendar-view-day'),
    (r'^add/$', 'add_reminder', {}, 'add-reminder'),
    (r'^add/(?P<year>[\d]+)/(?P<month>[\d]+)/(?P<day>[\d]+)/$', 'add_reminder_for_day', {}, 'add-reminder-for-day'),
    (r'^edit/(?P<slug>[\w-]+)/$', 'edit_reminder', {}, 'edit-reminder'),
    (r'^delete/(?P<slug>[\w-]+)/$', 'delete_reminder', {}, 'delete-reminder'),
    (r'^view/(?P<slug>[\w-]+)/$', 'view_reminder', {}, 'view-reminder'),
    (r'^dismiss/(?P<slug>[\w-]+)/$', 'dismiss_reminder', {}, 'dismiss-reminder'),
)
