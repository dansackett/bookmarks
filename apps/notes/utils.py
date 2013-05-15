import operator

from django.db.models import Q

from notes.models import Note


def total_notes(user):
    return Note.objects.filter(user=user).count()


def category_notes_count(user, category):
    return Note.objects.filter(user=user, category=category).count()


def get_category_data(user):
    # a dict with the slug as the key and a tuple as (name, icon, color, count)
    return {
        'no_category': ('No Category', 'icon-ban-circle', '#E64F48', category_notes_count(user, 'no_category'), 'no_category'),
        'bar': ('Bar', 'icon-beer', '#E88B3B', category_notes_count(user, 'bar'), 'bar'),
        'book': ('Book', 'icon-book', '#A7D4F1', category_notes_count(user, 'book'), 'book'),
        'food': ('Food', 'icon-food', '#2581D4', category_notes_count(user, 'food'), 'food'),
        'idea': ('Idea', 'icon-lightbulb', '#EAC050', category_notes_count(user, 'idea'), 'idea'),
        'movie': ('Movie', 'icon-film', '#1A48A8', category_notes_count(user, 'movie'), 'movie'),
        'music': ('Music', 'icon-music', '#A5249B', category_notes_count(user, 'music'), 'music'),
        'person': ('Person', 'icon-smile', '#0AA8EF', category_notes_count(user, 'person'), 'person'),
        'place': ('Place', 'icon-map-marker', '#C82750', category_notes_count(user, 'place'), 'place'),
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
