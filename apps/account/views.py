from django.shortcuts import render, redirect

from account.forms import ProfileForm

from tags.models import Tag


def home(request, template_name='account/home.html'):
    """Renders the home template for non logged in users"""
    context = {}
    return render(request, template_name, context)


def dashboard(request, template_name='account/account.html'):
    """Renders the home template for logged in users"""
    tags = Tag.objects.filter(user=request.user)

    context = {
        'tags': tags,
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
