import operator

from django.db.models import Q

from tags.models import Tag


def most_popular(user):
    tags = Tag.objects.filter(user=user).order_by('title')
    return sorted([(tag.bookmarks_count(tag), tag.title, tag) for tag in tags], reverse=True)


def total_tags(user):
    return Tag.objects.filter(user=user).count()


def search_tags(query_string, tags):
    if not query_string:
        return tags

    terms = query_string.split()

    title = tags.filter(reduce(operator.or_, (Q(title__icontains=term)
                               for term in terms)))
    desc = tags.filter(reduce(operator.or_, (Q(description__icontains=term)
                              for term in terms)))
    return list(set(title).union(set(desc)))
