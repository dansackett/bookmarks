import operator

from django.db.models import Q

from todolists.models import TodoList, Task


def total_todolists(user):
    return TodoList.objects.filter(user=user).count()


def search_todolists(query_string, todolists):
    if not query_string:
        return todolists

    terms = query_string.split()

    title = todolists.filter(reduce(operator.or_, (Q(title__icontains=term)
                             for term in terms)))
    return list(title)
