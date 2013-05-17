from datetime import datetime
from calendar import Calendar, SUNDAY

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from reminders.models import Reminder
from reminders.forms import NewReminderForm, EditReminderForm
from reminders.utils import search_reminders, get_next_and_previous, get_months


def list_reminders(request, template_name='reminders/list_reminders.html'):
    """Show a list of all reminders for a user"""
    reminders = Reminder.objects.filter(user=request.user, sent=False)
    reminders = reminders.order_by('date')

    if request.POST:
        reminders = search_reminders(request.POST.get('query', None), reminders)

    context = {
        'reminders': reminders,
    }
    return render(request, template_name, context)


def reminders_calendar(request, year=datetime.now().year, month=datetime.now().month,
                       template_name='reminders/calendar.html'):
    """Show a calendar of all reminders for a user"""
    month = int(month)
    year = int(year)
    months = get_months()
    years = [x for x in range(2013, 2030)]
    m = months[str(month)]
    # create a calendar starting with Sunday from last month
    cal = Calendar(SUNDAY)
    # get all the days in the calendar month and year specified
    days = [day for day in cal.itermonthdates(year, month)]
    # group the days into weeks going from Sunday to Saturday
    weeks = [days[i * 7:(i + 1) * 7] for i in range((len(days) / 7 + 1))]
    today = datetime.now().date()
    next_month, previous_month = get_next_and_previous(year, month)

    reminders = Reminder.objects.filter(user=request.user, sent=False)
    reminder_dates = [reminder.date.date() for reminder in reminders
                      if reminder.date.date().month == month]

    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        return redirect('calendar-date', year=selected_year, month=selected_month)

    context = {
        'weeks': weeks,
        'months': months,
        'today': today,
        'm': m,
        'year': year,
        'years': years,
        'next_month': next_month,
        'previous_month': previous_month,
        'reminders': reminders,
        'reminder_dates': reminder_dates,
    }
    return render(request, template_name, context)


def view_day_calendar(request, year, month, day,
                      template_name='reminders/view_reminders_for_day.html'):
    """Show a specific day from the calendar"""
    try:
        date = datetime(int(year), int(month), int(day)).date()
    except ValueError:
        raise Http404

    reminders = Reminder.objects.filter(user=request.user, sent=False)
    reminders_today = [reminder for reminder in reminders
                       if reminder.date.date() == date]

    context = {
        'reminders': reminders_today,
        'date': date,
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


def add_reminder_for_day(request, year, month, day, form_class=NewReminderForm,
                         template_name='reminders/add_reminder.html'):
    """Add a new reminder for a specific day"""
    try:
        date = datetime(int(year), int(month), int(day)).date()
    except ValueError:
        raise Http404

    form = form_class(request.POST or None, user=request.user, date=date)
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
        return redirect('list-reminders')

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
