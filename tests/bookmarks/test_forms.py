import datetime

from django.contrib.auth.models import User

import pytest

from bookmarks.forms import NewBookmarkForm, EditBookmarkForm
from bookmarks.models import Bookmark
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
def test_new_bookmark_form_is_valid():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    form = NewBookmarkForm({
        'title': 'test',
        'description': 'description',
        'url': 'http://www.google.com',
        'tags': tag.pk,
        'favorited': True,
    }, user=user)
    assert form.is_valid()


@pytest.mark.django_db
def test_new_bookmark_form_is_invalid_due_to_bad_url():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    form = NewBookmarkForm({
        'title': 'test',
        'description': 'description',
        'url': 'blah',
        'tags': tag.pk,
        'favorited': True,
    }, user=user)
    assert not form.is_valid()
    assert ['url'] == form.errors.keys()


@pytest.mark.django_db
def test_new_bookmark_form_is_invalid_because_bookmark_exists():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()
    form = NewBookmarkForm({
        'title': 'Test Bookmark',
        'description': 'description',
        'url': 'http://www.google.com',
        'tags': tag.pk,
        'favorited': True,
    }, user=user)
    assert not form.is_valid()
    assert ['title'] == form.errors.keys()


@pytest.mark.django_db
def test_new_bookmark_form_saves_correctly():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    form = NewBookmarkForm({
        'title': 'Test Bookmark',
        'description': 'description',
        'url': 'http://www.google.com',
        'tags': tag.pk,
        'favorited': True,
    }, user=user)
    assert form.is_valid()
    form.save()
    assert len(Bookmark.objects.all()) == 1


@pytest.mark.django_db
def test_edit_bookmark_form_is_valid():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()
    bookmark = Bookmark.objects.get(pk=1)
    form = EditBookmarkForm({
        'title': 'Test Bookmark',
        'description': 'description',
        'url': 'http://www.google.com',
        'tags': tag.pk,
        'favorited': True,
    }, user=user, bookmark=bookmark)
    assert form.is_valid()


@pytest.mark.django_db
def test_edit_bookmark_form_is_invalid_due_to_bad_url():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()
    bookmark = Bookmark.objects.get(pk=1)
    form = EditBookmarkForm({
        'title': 'Test Bookmark',
        'description': 'description',
        'url': 'blah',
        'tags': tag.pk,
        'favorited': True,
    }, user=user, bookmark=bookmark)
    assert not form.is_valid()
    assert ['url'] == form.errors.keys()


@pytest.mark.django_db
def test_edit_bookmark_form_is_invalid_because_bookmark_exists():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark1', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()
    Bookmark(title='Test Bookmark2', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()
    bookmark1 = Bookmark.objects.get(pk=1)
    form = EditBookmarkForm({
        'title': 'Test Bookmark2',
        'description': 'description',
        'url': 'http://www.google.com',
        'tags': tag.pk,
        'favorited': True,
    }, user=user, bookmark=bookmark1)
    assert not form.is_valid()
    assert ['title'] == form.errors.keys()


@pytest.mark.django_db
def test_edit_bookmark_form_saves_correctly():
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()
    bookmark = Bookmark.objects.get(pk=1)
    form = EditBookmarkForm({
        'title': 'Test Bookmark New',
        'description': 'description',
        'url': 'http://www.google.com',
        'tags': tag.pk,
        'favorited': True,
    }, user=user, bookmark=bookmark)
    assert form.is_valid()
    form.save()
    bookmark = Bookmark.objects.get(pk=1)
    assert bookmark.title == 'Test Bookmark New'
