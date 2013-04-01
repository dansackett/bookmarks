from django.core.urlresolvers import reverse

from bookmarks.utils import total_bookmarks, total_favorited
from tags.models import Tag
from tags.utils import total_tags, most_popular


def global_values(request):
    """Varianles available to all views"""
    if request.user.is_authenticated():
        return {
            'bookmarks_count': total_bookmarks(request.user),
            'tags_count': total_tags(request.user),
            'favorited_count': total_favorited(request.user),
            'all_tags': Tag.objects.filter(user=request.user),
            'popular_tags': most_popular(request.user)[:5],
            'referer': request.META.get('HTTP_REFERER', reverse('user-home')),
            'full_path': request.get_full_path(),
        }
    return {}
