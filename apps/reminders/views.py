from datetime import datetime
from calendar import Calendar, SUNDAY

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from mydash.utils import render_json
from reminders.models import Reminder
from reminders.forms import NewReminderForm, EditReminderForm
from reminders.utils import search_reminders, get_next_and_previous, get_months


def list_reminders(request):
    """Show a list of all reminders for a user"""
    reminders = Reminder.objects.filter(user=request.user, sent=False)
    reminders = reminders.order_by('date')

    if request.POST:
        reminders = search_reminders(request.POST.get('query', None), reminders)

    context = {
        'reminders': reminders,
    }
    return render(request, 'reminders/list_reminders.html', context)


def reminders_calendar(request, year=datetime.now().year, month=datetime.now().month):
    """Show a calendar of all reminders for a user"""
    month = int(month)
    year = int(year)
    months = get_months()
    today = datetime.now().date()

    # Set a set of year between now and 20 years in the future
    years = [x for x in range(datetime.now().year, datetime.now().year + 20)]
    # Get the selected month
    m = months[str(month)]
    # Create a calendar starting with Sunday from the last month
    cal = Calendar(SUNDAY)
    # Get all the days in the calendar month and year specified
    days = [day for day in cal.itermonthdates(year, month)]
    # Group the days into weeks going from Sunday to Saturday
    weeks = [days[i * 7:(i + 1) * 7] for i in range((len(days) / 7 + 1))]
    # Find the next and previous months
    next_month, previous_month = get_next_and_previous(year, month)

    # Get all of the reminders that happen in the current month
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
    return render(request, 'reminders/calendar.html', context)


def view_day_calendar(request, year, month, day):
    """Show a specific day from the calendar"""
    try:
        date = datetime(int(year), int(month), int(day)).date()
    except ValueError:
        raise Http404

    # Get reminders for the current day
    reminders = Reminder.objects.filter(user=request.user, sent=False)
    reminders_today = [reminder for reminder in reminders
                       if reminder.date.date() == date]

    context = {
        'reminders': reminders_today,
        'date': date,
    }
    return render(request, 'reminders/view_reminders_for_day.html', context)


def view_reminder(request, slug):
    """Show a reminder"""
    reminder = get_object_or_404(Reminder, user=request.user, slug=slug)

    context = {
        'reminder': reminder,
    }
    return render(request, 'reminders/view_reminder.html', context)


def add_reminder(request):
    """Add a new reminder"""
    form = NewReminderForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-reminders')

    context = {
        'form': form,
    }
    return render(request, 'reminders/add_reminder.html', context)


def add_reminder_for_day(request, year, month, day):
    """Add a new reminder for a specific day"""
    try:
        date = datetime(int(year), int(month), int(day)).date()
    except ValueError:
        raise Http404

    form = NewReminderForm(request.POST or None, user=request.user, date=date)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-reminders')

    context = {
        'form': form,
    }
    return render(request, 'reminders/add_reminder.html', context)


def edit_reminder(request, slug):
    """Edit an existing reminder"""
    reminder = get_object_or_404(Reminder, user=request.user, slug=slug)

    form = EditReminderForm(request.POST or None, user=request.user, instance=reminder)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-reminders')

    context = {
        'form': form,
        'reminder': reminder,
    }
    return render(request, 'reminders/edit_reminder.html', context)


@require_POST
def dismiss_reminder(request, slug):
    """Dismiss a reminder"""
    reminder = get_object_or_404(Reminder, user=request.user, slug=slug)

    reminder.dismissed = not reminder.dismissed
    reminder.save()
    return render_json(reminder.pk)


@require_POST
def delete_reminder(request, slug):
    """Delete a reminder"""
    reminder = get_object_or_404(Reminder, user=request.user, slug=slug)

    reminder_pk = reminder.pk
    reminder.delete()
    return render_json(reminder_pk)
