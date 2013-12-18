from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from mydash.utils import render_json
from notes.models import Note
from notes.forms import NewNoteForm, EditNoteForm
from notes.utils import search_notes, get_category_data


def list_categories(request):
    """Show a list of notes categories"""
    category_data = get_category_data(request.user)

    context = {
        'categories': category_data,
    }
    return render(request, 'notes/list_categories.html', context)


def view_category(request, category):
    """Show a list of notes for a category"""
    notes = Note.objects.filter(user=request.user, category=category)

    category_title = get_category_data(request.user)[category][0]

    if request.POST:
        notes = search_notes(request.POST.get('query', None), notes)

    context = {
        'notes': notes,
        'category': category,
        'category_title': category_title,
    }
    return render(request, 'notes/list_notes.html', context)


def view_note(request, category, slug):
    """Show a note"""
    note = get_object_or_404(Note, user=request.user, category=category, slug=slug)

    category = get_category_data(request.user)[category]

    context = {
        'note': note,
        'category': category,
    }
    return render(request, 'notes/view_note.html', context)


def add_note(request, category):
    """Add a new note"""
    form = NewNoteForm(request.POST or None, category=category, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        category = form.cleaned_data.get('category')
        return redirect('view-category', category=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'notes/add_note.html', context)


def edit_note(request, category, slug):
    """Edit an existing note"""
    note = get_object_or_404(Note, user=request.user, slug=slug)

    category = note.category

    form = EditNoteForm(request.POST or None, user=request.user, instance=note)

    if request.method == 'POST' and form.is_valid():
        form.save()
        category = form.cleaned_data.get('category')
        return redirect('view-category', category=category)

    context = {
        'note': note,
        'form': form,
        'category': category,
    }
    return render(request, 'notes/edit_note.html', context)


@require_POST
def delete_note(request, category, slug):
    """Delete a note"""
    note = get_object_or_404(Note, user=request.user, slug=slug)

    note_pk = note.pk
    note.delete()
    return render_json(note_pk)
