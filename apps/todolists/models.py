from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User


class TodoList(models.Model):
    """TodoList models"""
    title = models.CharField(max_length=100, verbose_name='List Name')
    slug = models.SlugField()
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        """Print the title as the representation of a todolist"""
        return self.title

    @permalink
    def get_absolute_url(self):
        """Return the view link for a todolist"""
        return ('view-todolist', (), {'slug': self.slug})

    @permalink
    def get_edit_url(self):
        """Return the edit link for a todolist"""
        return ('edit-todolist', (), {'slug': self.slug})

    @permalink
    def get_delete_url(self):
        """Return the delete link for a todolist"""
        return ('delete-todolist', (), {'slug': self.slug})

    def get_tasks(self):
        return Task.objects.filter(todolist=self)

    def get_tasks_count(self):
        return Task.objects.filter(todolist=self).count()

    def get_completed_tasks_count(self):
        return Task.objects.filter(todolist=self, complete=True).count()


class Task(models.Model):
    """TodoList Task models"""
    task = models.CharField(max_length=100, verbose_name='Task')
    slug = models.SlugField()
    user = models.ForeignKey(User)
    complete = models.BooleanField(default=False)
    todolist = models.ForeignKey(TodoList)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('modified_on',)

    def __unicode__(self):
        """Print the title as the representation of a task"""
        return self.task

    @permalink
    def get_edit_url(self):
        """Return the edit link for a task"""
        return ('edit-task', (), {'slug': self.todolist.slug, 'task_slug': self.slug})

    @permalink
    def get_delete_url(self):
        """Return the delete link for a task"""
        return ('delete-task', (), {'slug': self.todolist.slug, 'task_slug': self.slug})

    @permalink
    def get_complete_url(self):
        """Return the complete link for a task"""
        return ('complete-task', (), {'slug': self.todolist.slug, 'task_slug': self.slug})
