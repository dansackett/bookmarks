from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from mydash.utils import render_json
from bookmarks.models import Bookmark
from bookmarks.forms import NewBookmarkForm, EditBookmarkForm
from bookmarks.utils import search_bookmarks
from tags.models import Tag


def list_bookmarks(request):
    """Show a list of all bookmarks for a user"""
    bookmarks = Bookmark.objects.filter(user=request.user)

    if request.POST:
        bookmarks = search_bookmarks(request.POST.get('query', None), bookmarks)

    context = {
        'bookmarks': bookmarks,
    }
    return render(request, 'bookmarks/list_bookmarks.html', context)


def list_favorited_bookmarks(request):
    """Show a list of all favorited bookmarks for a user"""
    bookmarks = Bookmark.objects.filter(user=request.user, favorited=True)

    if request.POST:
        bookmarks = search_bookmarks(request.POST.get('query', None), bookmarks)

    context = {
        'bookmarks': bookmarks,
    }
    return render(request, 'bookmarks/list_favorited_bookmarks.html', context)


def add_bookmark(request, tag_slug=None):
    """Add a new bookmark"""
    if tag_slug:
        tag = get_object_or_404(Tag, user=request.user, slug=tag_slug)
    else:
        tag = None

    form = NewBookmarkForm(request.POST or None, tag=tag, user=request.user)

    if request.method == 'POST' and form.is_valid():
        bookmark = form.save()
        return redirect('view-tag', bookmark.tag.slug)

    context = {
        'form': form,
        'tag': tag,
    }
    return render(request, 'bookmarks/add_bookmark.html', context)


def edit_bookmark(request, slug, tag_slug):
    """Edit an existing bookmark"""
    tag = get_object_or_404(Tag, user=request.user, slug=tag_slug)
    bookmark = get_object_or_404(Bookmark, user=request.user, tag=tag, slug=slug)

    form = EditBookmarkForm(request.POST or None, user=request.user, instance=bookmark)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-tag', tag_slug)

    context = {
        'tag': tag,
        'bookmark': bookmark,
        'form': form,
    }
    return render(request, 'bookmarks/edit_bookmark.html', context)


@require_POST
def favorite_bookmark(request, slug, tag_slug):
    """Favorite a bookmark"""
    tag = get_object_or_404(Tag, user=request.user, slug=tag_slug)
    bookmark = get_object_or_404(Bookmark, user=request.user, tag=tag, slug=slug)

    bookmark.favorited = not bookmark.favorited
    bookmark.save()
    return render_json(bookmark.pk)


@require_POST
def delete_bookmark(request, slug, tag_slug):
    """Delete a bookmark"""
    tag = get_object_or_404(Tag, user=request.user, slug=tag_slug)
    bookmark = get_object_or_404(Bookmark, user=request.user, tag=tag, slug=slug)

    bookmark_pk = bookmark.pk
    bookmark.delete()
    return render_json(bookmark_pk)
