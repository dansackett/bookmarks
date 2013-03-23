from django.shortcuts import render
from django.views.decorators.http import require_POST

# from bookmarks.models import Bookmark
# from tags.models import Tag
# from bookmarks.forms import AddBookmarkForm, EditBookmarkForm


def list_bookmarks(request, tag_id,
                   template_name='bookmarks/list_bookmarks.html'):
    """Show a list of bookmarks for a specific tag"""

    context = {}
    return render(request, template_name, context)


def add_bookmark(request, tag_id, form_class='AddBookmarkForm',
                 template_name='bookmarks/add_bookmark.html'):
    """Add a new bookmark for a specific tag"""

    context = {}
    return render(request, template_name, context)


def edit_bookmark(request, tag_id, bookmark_id, form_class='EditBookmarkForm',
                  template_name='bookmarks/edit_bookmark.html'):
    """Edit an existing bookmark"""

    context = {}
    return render(request, template_name, context)


@require_POST
def delete_bookmark(request, tag_id, bookmark_id,
                    template_name='bookmarks/Delete_bookmark.html'):
    """Delete a bookmark"""

    context = {}
    return render(request, template_name, context)
