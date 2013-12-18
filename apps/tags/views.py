from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from bookmarks.models import Bookmark
from bookmarks.utils import search_bookmarks
from tags.models import Tag
from tags.forms import NewTagForm, EditTagForm
from tags.utils import search_tags


def list_tags(request):
    """Show a list of tags"""
    tags = Tag.objects.filter(user=request.user)

    if request.POST:
        tags = search_tags(request.POST.get('query', None), tags)

    context = {
        'tags': tags,
    }
    return render(request, 'tags/list_tags.html', context)


def view_tag(request, slug):
    """Show a tag's bookmarks"""
    tag = get_object_or_404(Tag, user=request.user, slug=slug)
    bookmarks = Bookmark.objects.filter(user=request.user, tag=tag)

    if request.POST:
        bookmarks = search_bookmarks(request.POST.get('query', None), bookmarks)

    context = {
        'bookmarks': bookmarks,
        'tag': tag,
    }
    return render(request, 'tags/view_tag.html', context)


def add_tag(request):
    """Add a new tag"""
    form = NewTagForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-tags')

    context = {
        'form': form,
    }
    return render(request, 'tags/add_tag.html', context)


def edit_tag(request, slug):
    """Edit an existing tag"""
    tag = get_object_or_404(Tag, user=request.user, slug=slug)

    form = EditTagForm(request.POST or None, user=request.user, instance=tag)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list-tags')

    context = {
        'tag': tag,
        'form': form,
    }
    return render(request, 'tags/edit_tag.html', context)


@require_POST
def delete_tag(request, slug):
    """Delete a tag"""
    tag = get_object_or_404(Tag, user=request.user, slug=slug)
    tag.delete()
    return redirect('list-tags')
