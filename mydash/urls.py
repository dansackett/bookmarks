from django.conf.urls import patterns, include


urlpatterns = patterns('',
    (r'^$', 'account.views.home', {}, 'home'),
    (r'^', include('auth.urls')),
    (r'^account/', include('account.urls')),
    (r'^tags/', include('tags.urls')),
    (r'^bookmarks/', include('bookmarks.urls')),
    (r'^reminders/', include('reminders.urls')),
    (r'^notes/', include('notes.urls')),
    (r'^todolists/', include('todolists.urls')),
)
