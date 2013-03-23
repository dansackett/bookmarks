import datetime

from django.contrib.auth.models import User

import pytest

from account.forms import ProfileForm


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
def test_profile_form_is_valid():
    user = make_users(1)[0]
    form = ProfileForm(user=user, data={
        'email': 'test@testers.com',
        'username': 'test-user0',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'password': 'P@ssw0rd!',
        'confirm_password': 'P@ssw0rd!',
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_form_is_not_valid_due_to_invalid_username():
    user = make_users(1)[0]
    form = ProfileForm(user=user, data={
        'email': 'test@testers.com',
        'username': 'test!user',
        'first_name': 'First Name',
        'last_name': 'Last Name',
    })
    assert not form.is_valid()
    assert ['username'] == form.errors.keys()


@pytest.mark.django_db
def test_profile_form_is_not_valid_due_to_username_taken():
    users = make_users(2)
    user2 = users[1]
    form = ProfileForm(user=user2, data={
        'email': 'test@testers.com',
        'username': 'test-user0',
        'first_name': 'First Name',
        'last_name': 'Last Name',
    })
    assert not form.is_valid()
    assert ['username'] == form.errors.keys()


@pytest.mark.django_db
def test_profile_form_is_valid_and_change_username():
    user = make_users(1)[0]
    form = ProfileForm(user=user, data={
        'email': 'test@testers.com',
        'username': 'test-user2',
        'first_name': 'First Name',
        'last_name': 'Last Name',
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_form_is_not_valid_due_to_bad_password():
    user = make_users(1)[0]
    form = ProfileForm(user=user, data={
        'email': 'test@testers.com',
        'username': 'test-user2',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'password': 'password',
        'confirm_password': 'pass',
    })
    assert not form.is_valid()
    assert ['password'] == form.errors.keys()


@pytest.mark.django_db
def test_profile_form_is_not_valid_due_to_passwords_dont_match():
    user = make_users(1)[0]
    form = ProfileForm(user=user, data={
        'email': 'test@testers.com',
        'username': 'test-user2',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'password': 'P@ssw0rd!',
        'confirm_password': 'pass',
    })
    assert not form.is_valid()
    assert ['__all__'] == form.errors.keys()


@pytest.mark.django_db
def test_profile_form_saves_correctly():
    user = make_users(1)[0]
    form = ProfileForm(user=user, data={
        'email': 'test@testers.com',
        'username': 'test-user1',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'password': 'P@ssw0rd!',
        'confirm_password': 'P@ssw0rd!',
    })
    assert form.is_valid()
    form.save()
    assert User.objects.all()[0].username == 'test-user1'


@pytest.mark.django_db
def test_profile_form_saves_correctly_with_password():
    user = make_users(1)[0]
    form = ProfileForm(user=user, data={
        'email': 'test@testers.com',
        'username': 'test-user1',
        'first_name': 'First Name',
        'last_name': 'Last Name',
    })
    assert form.is_valid()
    form.save()
    assert User.objects.all()[0].username == 'test-user1'
