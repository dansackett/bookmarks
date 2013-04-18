from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from reminders.models import Reminder
from reminders.forms import NewReminderForm, EditReminderForm
from reminders.utils import search_reminders


def list_reminders(request, template_name='reminders/list_reminders.html'):
    """Show a list of all reminders for a user"""
    reminders = Reminder.objects.filter(user=request.user)

    if request.POST:
        reminders = search_reminders(request.POST.get('query', None), reminders)

    context = {
        'reminders': reminders,
    }
    return render(request, template_name, context)


def view_reminder(request, slug, template_name='reminders/view_reminder.html'):
    """Show a reminder"""
    reminder = Reminder.objects.get(user=request.user, slug=slug)

    context = {
        'reminder': reminder,
    }
    return render(request, template_name, context)


def add_reminder(request, form_class=NewReminderForm,
                 template_name='reminders/add_reminder.html'):
    """Add a new reminder"""
    form = form_class(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-reminders')

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def edit_reminder(request, slug, form_class=EditReminderForm,
                  template_name='reminders/edit_reminder.html'):
    """Edit an existing reminder"""
    try:
        reminder = Reminder.objects.get(user=request.user, slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    form = form_class(request.POST or None, user=request.user, instance=reminder)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-reminder', slug)

    context = {
        'form': form,
        'reminder': reminder,
    }
    return render(request, template_name, context)


@require_POST
def dismiss_reminder(request, slug):
    """Dismiss a reminder"""
    reminder = Reminder.objects.get(user=request.user, slug=slug)
    reminder.dismissed = not reminder.dismissed
    reminder.save()
    return HttpResponse(reminder.pk)


@require_POST
def delete_reminder(request, slug):
    """Delete a reminder"""
    reminder = Reminder.objects.get(user=request.user, slug=slug)
    reminder.delete()
    return redirect('list-reminders')
