from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from mydash.utils import render_json
from bookmarks.models import Bookmark
from bookmarks.forms import NewBookmarkForm, EditBookmarkForm
from bookmarks.utils import search_bookmarks
from tags.models import Tag


def list_bookmarks(request, template_name='bookmarks/list_bookmarks.html'):
    """Show a list of all bookmarks for a user"""
    bookmarks = Bookmark.objects.filter(user=request.user)

    if request.POST:
        bookmarks = search_bookmarks(request.POST.get('query', None), bookmarks)

    context = {
        'bookmarks': bookmarks,
    }
    return render(request, template_name, context)


def list_favorited_bookmarks(request, template_name='bookmarks/list_favorited_bookmarks.html'):
    """Show a list of all favorited bookmarks for a user"""
    bookmarks = Bookmark.objects.filter(user=request.user, favorited=True)

    if request.POST:
        bookmarks = search_bookmarks(request.POST.get('query', None), bookmarks)

    context = {
        'bookmarks': bookmarks,
    }
    return render(request, template_name, context)


def add_bookmark(request, form_class=NewBookmarkForm,
                 template_name='bookmarks/add_bookmark.html'):
    """Add a new bookmark"""
    form = form_class(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-bookmarks')

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def edit_bookmark(request, slug, tag_slug, form_class=EditBookmarkForm,
                  template_name='bookmarks/edit_bookmark.html'):
    """Edit an existing bookmark"""
    try:
        tag = Tag.objects.get(user=request.user, slug=tag_slug)
        bookmark = Bookmark.objects.get(user=request.user, tag=tag, slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    form = form_class(request.POST or None, user=request.user, instance=bookmark)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-tag', tag_slug)

    context = {
        'tag': tag,
        'bookmark': bookmark,
        'form': form,
    }
    return render(request, template_name, context)


@require_POST
def favorite_bookmark(request, slug, tag_slug):
    """Favorite a bookmark"""
    tag = Tag.objects.get(user=request.user, slug=tag_slug)
    bookmark = Bookmark.objects.get(user=request.user, tag=tag, slug=slug)
    bookmark.favorited = not bookmark.favorited
    bookmark.save()
    return render_json(bookmark.pk)


@require_POST
def delete_bookmark(request, slug, tag_slug):
    """Delete a bookmark"""
    tag = Tag.objects.get(user=request.user, slug=tag_slug)
    bookmark = Bookmark.objects.get(user=request.user, tag=tag, slug=slug)
    bookmark.delete()
    return redirect('list-bookmarks')
