from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from bookmarks.models import Bookmark
from tags.models import Tag
from tags.forms import NewTagForm, EditTagForm


def list_tags(request, template_name='tags/list_tags.html'):
    """Show a list of tags"""
    tags = Tag.objects.filter(user=request.user)

    context = {
        'tags': tags,
    }
    return render(request, template_name, context)


def view_tag(request, slug, template_name='tags/view_tag.html'):
    """Show a tag's bookmarks"""
    try:
        tag = Tag.objects.get(user=request.user, slug=slug)
    except Tag.DoesNotExist:
        raise Http404

    bookmarks = Bookmark.objects.filter(user=request.user, tag=tag)

    context = {
        'bookmarks': bookmarks,
        'tag': tag,
    }
    return render(request, template_name, context)


def add_tag(request, form_class=NewTagForm,
            template_name='tags/add_tag.html'):
    """Add a new tag"""
    form = form_class(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user-home')

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def edit_tag(request, slug, form_class=EditTagForm,
             template_name='tags/edit_tag.html'):
    """Edit an existing tag"""
    try:
        tag = Tag.objects.get(user=request.user, slug=slug)
    except Tag.DoesNotExist:
        raise Http404

    form = form_class(request.POST or None, user=request.user, tag=tag)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user-home')

    context = {
        'tag': tag,
        'form': form,
    }
    return render(request, template_name, context)


@require_POST
def delete_tag(request, slug, template_name='tags/delete_tag.html'):
    """Delete a tag"""
    tag = Tag.objects.get(user=request.user, slug=slug)
    tag.delete()
    return redirect('user-home')
