from django.conf import settings
from django.conf.urls import patterns, include


urlpatterns = patterns('todolists.views',
    (r'^$', 'list_todolists', {}, 'list-todolists'),
    (r'^view/(?P<slug>[\w-]+)/$', 'view_todolist', {}, 'view-todolist'),
    (r'^view/(?P<slug>[\w-]+)/add-task/$', 'add_task', {}, 'add-task'),
    (r'^view/(?P<slug>[\w-]+)/edit-task/(?P<task_slug>[\w-]+)/$', 'edit_task', {}, 'edit-task'),
    (r'^view/(?P<slug>[\w-]+)/delete-task/(?P<task_slug>[\w-]+)/$', 'delete_task', {}, 'delete-task'),
    (r'^view/(?P<slug>[\w-]+)/complete-task/(?P<task_slug>[\w-]+)/$', 'complete_task', {}, 'complete-task'),
    (r'^add/$', 'add_todolist', {}, 'add-todolist'),
    (r'^edit/(?P<slug>[\w-]+)/$', 'edit_todolist', {}, 'edit-todolist'),
    (r'^delete/(?P<slug>[\w-]+)/$', 'delete_todolist', {}, 'delete-todolist'),
)
