from django.shortcuts import render, redirect
# from django.views.decorators.http import require_POST


def dashboard(request, template_name='account/account.html'):
    """Renders the home template for logged in users"""

    context = {}
    return render(request, template_name, context)
