from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from mydash.utils import render_json
from todolists.models import TodoList, Task
from todolists.forms import (
    NewTodoListForm,
    EditTodoListForm,
    NewTaskForm,
    EditTaskForm,
)
from todolists.utils import search_todolists


def list_todolists(request, template_name='todolists/list_todolists.html'):
    """Show a list of todolists"""
    todolists = TodoList.objects.filter(user=request.user).order_by('-modified_on')

    if request.POST:
        todolists = search_todolists(request.POST.get('query', None), todolists)

    context = {
        'todolists': todolists,
    }
    return render(request, template_name, context)


def view_todolist(request, slug, template_name='todolists/view_todolist.html'):
    """Show a todolist's tasks"""
    try:
        todolist = TodoList.objects.get(user=request.user, slug=slug)
    except TodoList.DoesNotExist:
        raise Http404

    tasks = Task.objects.filter(user=request.user, todolist=todolist)
    tasks = tasks.order_by('created_on')

    context = {
        'tasks': tasks,
        'todolist': todolist,
    }
    return render(request, template_name, context)


def add_todolist(request, form_class=NewTodoListForm,
                 template_name='todolists/add_todolist.html'):
    """Add a new todolist"""
    form = form_class(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-todolists')

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def edit_todolist(request, slug, form_class=EditTodoListForm,
             template_name='todolists/edit_todolist.html'):
    """Edit an existing todolist"""
    try:
        todolist = TodoList.objects.get(user=request.user, slug=slug)
    except TodoList.DoesNotExist:
        raise Http404

    form = form_class(request.POST or None, user=request.user, instance=todolist)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-todolists')

    context = {
        'todolist': todolist,
        'form': form,
    }
    return render(request, template_name, context)


@require_POST
def delete_todolist(request, slug):
    """Delete a todolist"""
    todolist = TodoList.objects.get(user=request.user, slug=slug)
    todolist_pk = todolist.pk
    todolist.delete()
    return render_json(todolist_pk)


def add_task(request, slug, form_class=NewTaskForm,
             template_name='todolists/add_task.html'):
    """Add a new task"""
    todolist = TodoList.objects.get(user=request.user, slug=slug)
    form = form_class(request.POST or None, user=request.user, todolist=todolist)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-todolist', todolist.slug)

    context = {
        'form': form,
        'todolist': todolist,
    }
    return render(request, template_name, context)


def edit_task(request, slug, task_slug, form_class=EditTaskForm,
              template_name='todolists/edit_task.html'):
    """Edit an existing task"""
    todolist = TodoList.objects.get(user=request.user, slug=slug)
    try:
        task = Task.objects.get(user=request.user, slug=task_slug, todolist=todolist)
    except Task.DoesNotExist:
        raise Http404

    form = form_class(request.POST or None, user=request.user, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-todolist', todolist.slug)

    context = {
        'todolist': todolist,
        'task': task,
        'form': form,
    }
    return render(request, template_name, context)


@require_POST
def delete_task(request, slug, task_slug):
    """Delete a task"""
    todolist = TodoList.objects.get(user=request.user, slug=slug)
    task = Task.objects.get(user=request.user, slug=task_slug, todolist=todolist)
    task_pk = task.pk
    task.delete()
    return render_json(task_pk)


@require_POST
def complete_task(request, slug, task_slug):
    """Complete a task"""
    todolist = TodoList.objects.get(user=request.user, slug=slug)
    task = Task.objects.get(user=request.user, slug=task_slug, todolist=todolist)
    task.complete = not task.complete
    task.save()
    return render_json(task.pk)
