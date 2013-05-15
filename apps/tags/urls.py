from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('tags.views',
    (r'^$', 'list_tags', {}, 'list-tags'),
    (r'^view/(?P<slug>[\w-]+)/$', 'view_tag', {}, 'view-tag'),
    (r'^add/$', 'add_tag', {}, 'add-tag'),
    (r'^edit/(?P<slug>[\w-]+)/$', 'edit_tag', {}, 'edit-tag'),
    (r'^delete/(?P<slug>[\w-]+)/$', 'delete_tag', {}, 'delete-tag'),
)
