from django.core.urlresolvers import reverse

from bookmarks.utils import total_bookmarks, total_favorited
from tags.models import Tag
from reminders.utils import total_reminders
from notes.utils import total_notes
from todolists.utils import total_todolists
from tags.utils import total_tags, most_popular


def global_values(request):
    """Varianles available to all views"""
    if request.user.is_authenticated():
        return {
            'bookmarks_count': total_bookmarks(request.user),
            'tags_count': total_tags(request.user),
            'favorited_count': total_favorited(request.user),
            'reminders_count': total_reminders(request.user),
            'notes_count': total_notes(request.user),
            'todolists_count': total_todolists(request.user),
            'all_tags': Tag.objects.filter(user=request.user),
            'popular_tags': most_popular(request.user)[:5],
            'full_path': request.get_full_path(),
        }
    return {}
