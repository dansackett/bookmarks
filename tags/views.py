from django.shortcuts import render
from django.views.decorators.http import require_POST

# from bookmarks.models import Bookmark
# from tags.models import Tag
# from tags.forms import AddTagForm, EditTagForm


def list_tags(request, template_name='tags/list_tags.html'):
    """Show a list of tags"""

    context = {}
    return render(request, template_name, context)


def add_tag(request, form_class='AddTagForm',
            template_name='tags/add_tag.html'):
    """Add a new tag"""

    context = {}
    return render(request, template_name, context)


def edit_tag(request, tag_id, form_class='EditTagForm',
             template_name='tags/edit_tag.html'):
    """Edit an existing tag"""

    context = {}
    return render(request, template_name, context)


@require_POST
def delete_tag(request, tag_id, template_name='tags/delete_tag.html'):
    """Delete a tag"""

    context = {}
    return render(request, template_name, context)
