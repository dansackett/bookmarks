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


@pytest.mark.parametrize('url', [
    '/account/',
    '/account/profile/edit/',
    '/tags/',
    '/bookmarks/',
])
def test_anonymous_user_cannot_access_internal_urls(url, client):
    response = client.get(url)
    assert response.status_code == 302
    assert response['location'].endswith('/login/')


@pytest.mark.parametrize('url', [
    '/login/',
    '/register/',
])
def test_anonymous_user_can_access_public_urls(url, client):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize('url', [
    '/login/',
    '/register/',
])
@pytest.mark.django_db
def test_authenticated_user_cannot_access_public_urls(url, client):
    user = make_users(1)[0]
    assert client.login(username=user.username, password='P@ssw0rd!')
    response = client.get(url)
    assert response.status_code == 302
    assert response['location'].endswith('/account/')


@pytest.mark.parametrize('url', [
    '/account/',
    '/account/profile/edit/',
    '/tags/',
    '/bookmarks/',
])
@pytest.mark.django_db
def test_anonymous_user_can_access_internal_urls(url, client):
    user = make_users(1)[0]
    assert client.login(username=user.username, password='P@ssw0rd!')
    response = client.get(url)
    assert response.status_code == 200
