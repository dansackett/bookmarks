import datetime

import pytest

from django.contrib.auth.models import User

from tags.models import Tag
from bookmarks.models import Bookmark


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
def test_bookmarks_count_without_args():
    user = make_users(1)[0]
    Tag(title='Test Tag', slug='test-tag', user=user).save()
    tag = Tag.objects.get(pk=1)
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tag=tag, url='http://www.google.com').save()
    assert tag.bookmarks_count() == 1


@pytest.mark.django_db
def test_bookmarks_count_with_args():
    users = make_users(1)
    user = users[0]
    Tag(title='Test Tag', slug='test-tag', user=user).save()
    Tag(title='Test Tag2', slug='test-tag2', user=user).save()
    tag = Tag.objects.get(pk=1)
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tag=tag, url='http://www.google.com').save()
    bookmark = Bookmark.objects.get(pk=1)
    assert tag.bookmarks_count(tag=tag) == 1


@pytest.mark.django_db
def test_tags_unicode_method_returns_title_correctly():
    user = make_users(1)[0]
    Tag(title='Test Tag', slug='test-tag', user=user).save()
    tag = Tag.objects.get(pk=1)
    assert tag.__unicode__() == 'Test Tag'


@pytest.mark.django_db
def test_tags_get_absolute_url_returns_correct_url():
    user = make_users(1)[0]
    Tag(title='Test Tag', slug='test-tag', user=user).save()
    tag = Tag.objects.get(pk=1)
    assert tag.get_absolute_url() == '/tags/view/test-tag/'


@pytest.mark.django_db
def test_tags_get_edit_url_returns_correct_url():
    user = make_users(1)[0]
    Tag(title='Test Tag', slug='test-tag', user=user).save()
    tag = Tag.objects.get(pk=1)
    assert tag.get_edit_url() == '/tags/edit/test-tag/'


@pytest.mark.django_db
def test_tags_get_delete_url_returns_correct_url():
    user = make_users(1)[0]
    Tag(title='Test Tag', slug='test-tag', user=user).save()
    tag = Tag.objects.get(pk=1)
    assert tag.get_delete_url() == '/tags/delete/test-tag/'
