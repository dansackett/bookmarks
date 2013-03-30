from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from auth.forms import LoginForm, RegistrationForm


def login(request, template_name='auth/home.html', form_class=LoginForm):
    """Renders the home/login template"""
    form = form_class(request.POST or None)
    error = ''
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('user-home')
        else:
            error = 'Your username or password appear to be incorrect.'

    context = {
        'form': form,
        'error': error,
    }
    return render(request, template_name, context)


@require_POST
def logout(request):
    """Logout a user"""
    auth.logout(request)
    return redirect('login')


def register(request, template_name='auth/register.html',
             form_class=RegistrationForm):
    """Allow a user to register for the site"""
    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('user-home')
        return redirect('login')

    context = {
        'form': form,
    }
    return render(request, template_name, context)
