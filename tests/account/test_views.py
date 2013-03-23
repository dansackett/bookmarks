import datetime

from django.contrib.auth.models import User

import pytest


def make_users(number):
    # setup user
    for i in range(number):
        user = User(
            username='test-user' + str(i),
            first_name='First Name',
            last_name='Last Name',
            email='test@testers.com',
            is_active=True,
            is_staff=False,
            date_joined=datetime.datetime.now(),
        )
        user.set_password('P@ssw0rd!')
        user.save()

    return User.objects.all()


@pytest.mark.django_db
def test_dashboard_renders(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    assert client.login(username=user.username, password=password)
    assert client.get('/account/')


@pytest.mark.django_db
def test_view_profile_renders(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    assert client.login(username=user.username, password=password)
    assert client.get('/account/profile/')


@pytest.mark.django_db
def test_edit_profile_renders(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    assert client.login(username=user.username, password=password)
    assert client.get('/account/profile/edit/')


@pytest.mark.django_db
def test_edit_profile_form_works(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    assert client.login(username=user.username, password=password)
    assert client.get('/account/profile/edit/')
    post_response = client.post('/account/profile/edit/', data={
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    })
    assert post_response.status_code == 302
