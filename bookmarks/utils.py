from bookmarks.models import Bookmark


def favorited(user):
    bookmarks = Bookmark.objects.filter(user=user, favorited=True)
    return bookmarks.order_by('modified_on')


def most_recent(user):
    return Bookmark.objects.filter(user=user).order_by('-modified_on')
