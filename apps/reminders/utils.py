import operator

from django.db.models import Q
from django.core.urlresolvers import reverse

from reminders.models import Reminder


def total_reminders(user):
    return Reminder.objects.filter(user=user).count()


def get_months():
    return {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }


def get_next_and_previous(year, month):
    # If it's January...
    if month == 1:
        next_month = reverse(
            'calendar-date',
            kwargs={'year': '{}'.format(year), 'month': '{}'.format(month + 1)}
        )
        previous_month = reverse(
            'calendar-date',
            kwargs={'year': '{}'.format(year - 1), 'month': '12'}
        )
    # If it's December
    elif month == 12:
        next_month = reverse(
            'calendar-date',
            kwargs={'year': '{}'.format(year + 1), 'month': '1'}
        )
        previous_month = reverse(
            'calendar-date',
            kwargs={'year': '{}'.format(year), 'month': '{}'.format(month - 1)}
        )
    # If it's any other month
    elif month < 12:
        next_month = reverse(
            'calendar-date',
            kwargs={'year': '{}'.format(year), 'month': '{}'.format(month + 1)}
        )
        previous_month = reverse(
            'calendar-date',
            kwargs={'year': '{}'.format(year), 'month': '{}'.format(month - 1)}
        )

    return next_month, previous_month


def search_reminders(query_string, reminders):
    if not query_string:
        return reminders

    terms = query_string.split()

    title = reminders.filter(reduce(operator.or_,
                                    (Q(title__icontains=term)
                                     for term in terms)))
    desc = reminders.filter(reduce(operator.or_,
                                   (Q(description__icontains=term)
                                    for term in terms)))
    return list(set(title).union(set(desc)))
