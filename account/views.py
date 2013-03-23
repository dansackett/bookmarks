from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from account.forms import ProfileForm


def dashboard(request, template_name='account/account.html'):
    """Renders the home template for logged in users"""

    context = {}
    return render(request, template_name, context)


def view_profile(request, template_name='account/view_profile.html'):
    """Shows your profile"""
    context = {}
    return render(request, template_name, context)


def edit_profile(request, form_class=ProfileForm,
                 template_name='account/edit_profile.html'):
    """Edit your profile"""
    form = form_class(request.POST or None, user=request.user)
    cleaned_data = ''
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('view-profile')

    context = {
        'form': form,
    }
    return render(request, template_name, context)
