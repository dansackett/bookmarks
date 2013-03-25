from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('bookmarks.views',
    (r'^$', 'list_bookmarks', {}, 'list-bookmarks'),
    (r'^add/(?P<tag_slug>[\w-]+)/$', 'add_bookmark', {}, 'add-bookmark'),
    (r'^edit/(?P<tag_slug>[\w-]+)/(?P<slug>[\w-]+)/$', 'edit_bookmark', {}, 'edit-bookmark'),
    (r'^delete/(?P<tag_slug>[\w-]+)/(?P<slug>[\w-]+)/$', 'delete_bookmark', {}, 'delete-bookmark'),
)
