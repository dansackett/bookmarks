import datetime

from django.contrib.auth.models import User

import pytest

from tags.forms import NewTagForm, EditTagForm
from tags.models import Tag


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
def test_new_tag_form_is_valid():
    user = make_users(1)[0]
    form = NewTagForm({
        'title': 'test',
    }, user=user)
    assert form.is_valid()


@pytest.mark.django_db
def test_new_tag_form_is_invalid_due_to_no_title():
    user = make_users(1)[0]
    form = NewTagForm({
        'title': '',
    }, user=user)
    assert not form.is_valid()
    assert ['title'] == form.errors.keys()


@pytest.mark.django_db
def test_new_tag_form_is_invalid_due_to_tag_exists():
    user = make_users(1)[0]
    Tag(title='title', user=user).save()
    form = NewTagForm({
        'title': 'title',
    }, user=user)
    assert not form.is_valid()
    assert ['title'] == form.errors.keys()


@pytest.mark.django_db
def test_new_tag_form_saves_correctly():
    user = make_users(1)[0]
    form = NewTagForm({
        'title': 'title',
    }, user=user)
    assert form.is_valid()
    form.save()
    assert len(Tag.objects.all()) == 1


@pytest.mark.django_db
def test_edit_tag_form_is_valid():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    form = EditTagForm({
        'title': 'test',
    }, user=user, tag=tag)
    assert form.is_valid()


@pytest.mark.django_db
def test_edit_tag_form_is_invalid_due_to_no_title():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    form = EditTagForm({
        'title': '',
    }, user=user, tag=tag)
    assert not form.is_valid()
    assert ['title'] == form.errors.keys()


@pytest.mark.django_db
def test_edit_tag_form_is_invalid_due_to_tag_exists():
    user = make_users(1)[0]
    Tag(title='tag1', user=user).save()
    tag = Tag(title='tag2', user=user)
    tag.save()
    form = EditTagForm({
        'title': 'tag1',
    }, user=user, tag=tag)
    assert not form.is_valid()
    assert ['title'] == form.errors.keys()



@pytest.mark.django_db
def test_edit_tag_form_allows_same_tag_name_to_save():
    user = make_users(1)[0]
    tag = Tag(title='tag', user=user)
    tag.save()
    form = EditTagForm({
        'title': 'tag',
    }, user=user, tag=tag)
    assert form.is_valid()
    form.save()
    assert Tag.objects.get(pk=1).title == 'tag'

@pytest.mark.django_db
def test_edit_tag_form_saves_correctly():
    user = make_users(1)[0]
    tag = Tag(title='tag', user=user)
    tag.save()
    form = EditTagForm({
        'title': 'new name',
    }, user=user, tag=tag)
    assert form.is_valid()
    form.save()
    assert Tag.objects.get(pk=1).title == 'new name'
