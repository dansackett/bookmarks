from django.shortcuts import render, redirect

from account.forms import ProfileForm

from tags.models import Tag


def home(request):
    """Renders the home template for non logged in users"""
    context = {}
    return render(request, 'account/home.html', context)


def dashboard(request):
    """Renders the home template for logged in users"""
    tags = Tag.objects.filter(user=request.user)

    context = {
        'tags': tags,
    }
    return render(request, 'account/account.html', context)


def edit_profile(request):
    """Edit your profile"""
    form = ProfileForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user-home')

    context = {
        'form': form,
    }
    return render(request, 'account/edit_profile.html', context)
