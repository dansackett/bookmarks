from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from bookmarks.models import Bookmark
from bookmarks.forms import NewBookmarkForm, EditBookmarkForm
from tags.models import Tag


def list_bookmarks(request, favorited=False, template_name='bookmarks/list_bookmarks.html'):
    """Show a list of all bookmarks for a user"""
    if favorited:
        bookmarks = Bookmark.objects.filter(user=request.user, favorited=True)
    else:
        bookmarks = Bookmark.objects.filter(user=request.user)

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
        return redirect('user-home')

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def edit_bookmark(request, slug, tag_slug, form_class=EditBookmarkForm,
                  template_name='bookmarks/edit_bookmark.html'):
    """Edit an existing bookmark"""
    try:
        tag = Tag.objects.get(user=request.user, slug=tag_slug)
        bookmark = Bookmark.objects.get(user=request.user, tags=tag, slug=slug)
    except ObjectDoesNotExist:
        raise Http404

    form = form_class(request.POST or None, user=request.user,
                      bookmark=bookmark)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-tag', tag_slug)

    context = {
        'tag': tag,
        'form': form,
    }
    return render(request, template_name, context)


@require_POST
def delete_bookmark(request, slug, tag_slug,
                    template_name='bookmarks/Delete_bookmark.html'):
    """Delete a bookmark"""
    tag = Tag.objects.get(user=request.user, slug=tag_slug)
    bookmark = Bookmark.objects.get(user=request.user, tags=tag, slug=slug)
    bookmark.delete()
    return redirect('user-home')
