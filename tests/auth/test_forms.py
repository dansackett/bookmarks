import datetime

from django.contrib.auth.models import User

import pytest

from auth.forms import LoginForm, RegistrationForm


def test_login_form_is_valid():
    form = LoginForm({
        'username': 'test',
        'password': 'password',
    })
    assert form.is_valid()


def test_login_form_is_not_valid():
    form = LoginForm({
        'username': '',
        'password': 'password',
    })
    assert not form.is_valid()


@pytest.mark.django_db
def test_registration_form_is_valid():
    form = RegistrationForm({
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'username': 'test',
        'password': 'P@ssw0rd!',
        'confirm_password': 'P@ssw0rd!',
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_registration_form_is_not_valid_due_to_username_being_taken():
    # setup user
    user = User(
        username='test-user',
        first_name='First Name',
        last_name='Last Name',
        email='test@testers.com',
        is_active=True,
        is_staff=False,
        date_joined=datetime.datetime.now(),
    )
    user.set_password('P@ssw0rd!')
    user.save()

    form = RegistrationForm({
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'username': 'test-user',
        'password': 'P@ssw0rd!',
        'confirm_password': 'P@ssw0rd!',
    })
    assert not form.is_valid()
    assert ['username'] == form.errors.keys()


@pytest.mark.django_db
def test_registration_form_is_not_valid_due_to_bad_password():
    form = RegistrationForm({
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'username': 'test-user',
        'password': 'pass',
        'confirm_password': 'pass',
    })
    assert not form.is_valid()
    assert ['password'] == form.errors.keys()


@pytest.mark.django_db
def test_registration_form_is_not_valid_due_to_confirm_password_missing():
    form = RegistrationForm({
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'username': 'test-user',
        'password': 'P@ssw0rd!',
    })
    assert not form.is_valid()
    assert ['confirm_password'] == form.errors.keys()


@pytest.mark.django_db
def test_registration_form_is_not_valid_due_to_passwords_dont_match():
    form = RegistrationForm({
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'username': 'test-user',
        'password': 'P@ssw0rd!',
        'confirm_password': 'pass',
    })
    assert not form.is_valid()
    assert ['__all__'] == form.errors.keys()


@pytest.mark.django_db
def test_registration_form_creates_user():
    form = RegistrationForm({
        'email': 'test@testers.com',
        'first_name': 'Dan',
        'last_name': 'Sackett',
        'username': 'test',
        'password': 'P@ssw0rd!',
        'confirm_password': 'P@ssw0rd!',
    })
    assert form.is_valid()
    form.save()
    assert len(User.objects.all()) == 1
