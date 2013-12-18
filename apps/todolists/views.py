from django.shortcuts import render, redirect, get_object_or_404
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


def list_todolists(request):
    """Show a list of todolists"""
    todolists = TodoList.objects.filter(user=request.user).order_by('-modified_on')

    if request.POST:
        todolists = search_todolists(request.POST.get('query', None), todolists)

    context = {
        'todolists': todolists,
    }
    return render(request, 'todolists/list_todolists.html', context)


def view_todolist(request, slug):
    """Show a todolist's tasks"""
    todolist = get_object_or_404(TodoList, user=request.user, slug=slug)

    tasks = Task.objects.filter(user=request.user, todolist=todolist)
    tasks = tasks.order_by('created_on')

    context = {
        'tasks': tasks,
        'todolist': todolist,
    }
    return render(request, 'todolists/view_todolist.html', context)


def add_todolist(request):
    """Add a new todolist"""
    form = NewTodoListForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-todolists')

    context = {
        'form': form,
    }
    return render(request, 'todolists/add_todolist.html', context)


def edit_todolist(request, slug):
    """Edit an existing todolist"""
    todolist = get_object_or_404(TodoList, user=request.user, slug=slug)

    form = EditTodoListForm(request.POST or None, user=request.user, instance=todolist)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-todolists')

    context = {
        'todolist': todolist,
        'form': form,
    }
    return render(request, 'todolists/edit_todolist.html', context)


@require_POST
def delete_todolist(request, slug):
    """Delete a todolist"""
    todolist = get_object_or_404(TodoList, user=request.user, slug=slug)

    todolist_pk = todolist.pk
    todolist.delete()
    return render_json(todolist_pk)


def add_task(request, slug):
    """Add a new task"""
    todolist = get_object_or_404(TodoList, user=request.user, slug=slug)

    form = NewTaskForm(request.POST or None, user=request.user, todolist=todolist)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-todolist', todolist.slug)

    context = {
        'form': form,
        'todolist': todolist,
    }
    return render(request, 'todolists/add_task.html', context)


def edit_task(request, slug, task_slug):
    """Edit an existing task"""
    todolist = get_object_or_404(TodoList, user=request.user, slug=slug)
    task = get_object_or_404(Task, user=request.user, slug=task_slug, todolist=todolist)

    form = EditTaskForm(request.POST or None, user=request.user, instance=task)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-todolist', todolist.slug)

    context = {
        'todolist': todolist,
        'task': task,
        'form': form,
    }
    return render(request, 'todolists/edit_task.html', context)


@require_POST
def delete_task(request, slug, task_slug):
    """Delete a task"""
    todolist = get_object_or_404(TodoList, user=request.user, slug=slug)
    task = get_object_or_404(Task, user=request.user, slug=task_slug, todolist=todolist)

    task_pk = task.pk
    task.delete()
    return render_json(task_pk)


@require_POST
def complete_task(request, slug, task_slug):
    """Complete a task"""
    todolist = get_object_or_404(TodoList, user=request.user, slug=slug)
    task = get_object_or_404(Task, user=request.user, slug=task_slug, todolist=todolist)

    task.complete = not task.complete
    task.save()
    return render_json(task.pk)
