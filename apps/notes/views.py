from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from bookmarks.models import Bookmark
from bookmarks.utils import search_bookmarks
from notes.models import Note
from notes.forms import NewNoteForm, EditNoteForm
from notes.utils import search_notes, get_category_data


def list_categories(request, template_name='notes/list_categories.html'):
    """Show a list of notes categories"""
    category_data = get_category_data(request.user)

    context = {
        'categories': category_data,
    }
    return render(request, template_name, context)


def view_category(request, category, template_name='notes/list_notes.html'):
    """Show a list of notes for a category"""
    notes = Note.objects.filter(user=request.user, category=category)

    category = get_category_data(request.user)[category]

    if request.POST:
        notes = search_notes(request.POST.get('query', None), notes)

    context = {
        'notes': notes,
        'category': category,
    }
    return render(request, template_name, context)


def view_note(request, category, slug, template_name='notes/view_note.html'):
    """Show a note"""
    try:
        note = Note.objects.get(user=request.user, category=category, slug=slug)
    except Note.DoesNotExist:
        raise Http404

    category = get_category_data(request.user)[category]

    context = {
        'note': note,
        'category': category,
    }
    return render(request, template_name, context)


def add_note(request, form_class=NewNoteForm, template_name='notes/add_note.html'):
    """Add a new note"""
    form = form_class(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        category = form.cleaned_data.get('category')
        return redirect('view-category', category=category)

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def edit_note(request, category, slug, form_class=EditNoteForm,
             template_name='notes/edit_note.html'):
    """Edit an existing note"""
    try:
        note = Note.objects.get(user=request.user, slug=slug)
    except Note.DoesNotExist:
        raise Http404

    form = form_class(request.POST or None, user=request.user, instance=note)
    if request.method == 'POST' and form.is_valid():
        form.save()
        category = form.cleaned_data.get('category')
        return redirect('view-category', category=category)

    context = {
        'note': note,
        'form': form,
    }
    return render(request, template_name, context)


@require_POST
def delete_note(request, category, slug):
    """Delete a note"""
    note = Note.objects.get(user=request.user, slug=slug)
    note.delete()
    return redirect('list-categories')
