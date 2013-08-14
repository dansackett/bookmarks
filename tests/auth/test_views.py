import datetime

from django.contrib.auth.models import User

import pytest

from auth.forms import LoginForm, RegistrationForm


def create_user():
    # setup user
    username = 'test-username'
    password = 'P@ssw0rd!'
    user = User(
        username=username,
        first_name='First Name',
        last_name='Last Name',
        email='test@testers.com',
        is_active=True,
        is_staff=False,
        date_joined=datetime.datetime.now(),
    )
    user.set_password(password)
    user.save()
    return username, password


@pytest.mark.django_db
def test_user_can_login(client):
    username, password = create_user()
    post_response = client.post('/login/', data={
        'username': username,
        'password': password,
    })
    assert post_response.status_code == 302
    assert post_response['location'].endswith('/account/')


@pytest.mark.django_db
def test_user_cannot_login_because_of_no_username(client):
    username, password = create_user()
    post_response = client.post('/login/', data={
        'username': '',
        'password': password,
    })
    assert ['username'] == post_response.context['form'].errors.keys()


@pytest.mark.django_db
def test_user_cannot_login_because_of_bad_username(client):
    username, password = create_user()
    post_response = client.post('/login/', data={
        'username': 'bad-username',
        'password': password,
    })
    error_message = 'Your username or password appear to be incorrect.'
    assert post_response.context['error'] == error_message


@pytest.mark.django_db
def test_user_cannot_directly_access_logout_with_get_request(client):
    username, password = create_user()
    client.login(username=username, password=password)
    response = client.get('/logout/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_user_can_logout(client):
    username, password = create_user()
    client.login(username=username, password=password)
    post_response = client.post('/logout/')
    assert post_response['location'].endswith('/')


@pytest.mark.django_db
def test_user_can_register(client):
    post_response = client.post('/register/', data={
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'username': 'test',
        'password': 'P@ssw0rd!',
        'confirm_password': 'P@ssw0rd!',
    })
    assert post_response.status_code == 302
    assert post_response['location'].endswith('/account/')


@pytest.mark.django_db
def test_user_cannot_register_due_to_missing_username(client):
    post_response = client.post('/register/', data={
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'password': 'P@ssw0rd!',
        'confirm_password': 'P@ssw0rd!',
    })
    assert ['username'] == post_response.context['form'].errors.keys()
