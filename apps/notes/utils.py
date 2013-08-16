import operator

from django.db.models import Q

from notes.models import Note


def total_notes(user):
    return Note.objects.filter(user=user).count()


def category_notes_count(user, category):
    return Note.objects.filter(user=user, category=category).count()


def get_category_data(user):
    # a dict with the slug as the key and a tuple as (name, count)
    return {
        'no_category': ('No Category', category_notes_count(user, 'no_category')),
        'bar': ('Bar', category_notes_count(user, 'bar')),
        'book': ('Book', category_notes_count(user, 'book')),
        'food': ('Food', category_notes_count(user, 'food')),
        'idea': ('Idea', category_notes_count(user, 'idea')),
        'movie': ('Movie', category_notes_count(user, 'movie')),
        'music': ('Music', category_notes_count(user, 'music')),
        'person': ('Person', category_notes_count(user, 'person')),
        'place': ('Place', category_notes_count(user, 'place')),
    }


def search_notes(query_string, notes):
    if not query_string:
        return notes

    terms = query_string.split()

    title = notes.filter(reduce(operator.or_, (Q(title__icontains=term)
                                for term in terms)))
    desc = notes.filter(reduce(operator.or_, (Q(description__icontains=term)
                               for term in terms)))
    return list(set(title).union(set(desc)))
