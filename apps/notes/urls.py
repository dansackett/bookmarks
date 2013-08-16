from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('notes.views',
    (r'^categories/$', 'list_categories', {}, 'list-categories'),
    (r'^category/(?P<category>[\w-]+)/$', 'view_category', {}, 'view-category'),
    (r'^view/(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', 'view_note', {}, 'view-note'),
    (r'^add/(?P<category>[\w-]+)/$', 'add_note', {}, 'add-note'),
    (r'^edit/(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', 'edit_note', {}, 'edit-note'),
    (r'^delete/(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', 'delete_note', {}, 'delete-note'),
)
