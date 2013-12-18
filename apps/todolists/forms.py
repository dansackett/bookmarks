from django import forms
from django.template.defaultfilters import slugify

from todolists.models import TodoList, Task


class BaseTodoListForm(forms.ModelForm):

    class Meta:
        model = TodoList
        exclude = ('slug', 'user')


class NewTodoListForm(BaseTodoListForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewTodoListForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if TodoList.objects.filter(title=title, user=self.user):
            raise forms.ValidationError('You already have a list with that title.')

        return title

    def save(self, commit=True):
        todolist = super(NewTodoListForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        todolist.slug = slugify(title)
        todolist.user = self.user
        todolist.save()

        return todolist


class EditTodoListForm(BaseTodoListForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditTodoListForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if self.instance.title != title:
            if TodoList.objects.filter(title=title, user=self.user):
                raise forms.ValidationError('You already have a todolist with that title.')

        return title

    def save(self, commit=True):
        todolist = super(EditTodoListForm, self).save(commit=False)
        title = self.cleaned_data.get('title')
        todolist = self.instance
        todolist.slug = slugify(title)
        todolist.user = self.user
        todolist.save()

        return todolist


class BaseTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('slug', 'user', 'complete', 'todolist',)


class NewTaskForm(BaseTaskForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.todolist = kwargs.pop('todolist', None)
        super(NewTaskForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_task(self):
        task = self.cleaned_data.get('task')

        if Task.objects.filter(task=task, user=self.user, todolist=self.todolist):
            raise forms.ValidationError('That\'s already a task.')

        return task

    def save(self, commit=True):
        task = super(NewTaskForm, self).save(commit=False)
        task_title = self.cleaned_data.get('task')
        task.slug = slugify(task_title)
        task.user = self.user
        task.todolist = self.todolist
        task.save()

        return task


class EditTaskForm(BaseTaskForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.todolist = kwargs.pop('todolist', None)
        super(EditTaskForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_task(self):
        task = self.cleaned_data.get('task')

        if self.instance.task != task:
            if Task.objects.filter(task=task, user=self.user, todolist=self.todolist):
                raise forms.ValidationError('That\'s already a task.')

        return task

    def save(self, commit=True):
        task = super(EditTaskForm, self).save(commit=False)
        task_title = self.cleaned_data.get('task')
        task = self.instance
        task.slug = slugify(task_title)
        task.save()

        return task
