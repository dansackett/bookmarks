import operator

from django.db.models import Q

from reminders.models import Reminder


def total_reminders(user):
    return Reminder.objects.filter(user=user).count()


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
