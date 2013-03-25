from tags.models import Tag


def most_popular(user):
    tags = Tag.objects.filter(user=user)
    return sorted([(tag.bookmarks_count(tag), tag) for tag in tags], reverse=True)
