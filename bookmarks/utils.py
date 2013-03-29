import operator

from django.db.models import Q

from bookmarks.models import Bookmark


def favorited(user):
    bookmarks = Bookmark.objects.filter(user=user, favorited=True)
    return bookmarks.order_by('modified_on')


def most_recent(user):
    return Bookmark.objects.filter(user=user).order_by('-modified_on')


def total_bookmarks(user):
    return Bookmark.objects.filter(user=user).count()


def total_favorited(user):
    return favorited(user).count()


def search_bookmarks(query_string, bookmarks):
    if not query_string:
        return bookmarks

    terms = query_string.split()

    title = bookmarks.filter(reduce(operator.or_,
                                    (Q(title__icontains=term)
                                     for term in terms)))
    desc = bookmarks.filter(reduce(operator.or_,
                                    (Q(description__icontains=term)
                                     for term in terms)))
    return list(set(title).union(set(desc)))
