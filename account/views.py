from django.shortcuts import render, redirect

from account.forms import ProfileForm
from tags.utils import most_popular
from bookmarks.utils import most_recent


def dashboard(request, template_name='account/account.html'):
    """Renders the home template for logged in users"""
    new_bookmarks = most_recent(request.user)[:5]

    context = {
        'new_bookmarks': new_bookmarks,
    }
    return render(request, template_name, context)


def edit_profile(request, form_class=ProfileForm,
                 template_name='account/edit_profile.html'):
    """Edit your profile"""
    form = form_class(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user-home')

    context = {
        'form': form,
    }
    return render(request, template_name, context)
