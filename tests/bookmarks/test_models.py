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
def test_bookmarks_unicode_method_returns_title_correctly():
    user = make_users(1)[0]
    tag = Tag(title='Test Tag', slug='test-tag', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', tag=tag,
             url="http://www.testers.com", user=user).save()
    bookmark = Bookmark.objects.get(pk=1)
    assert bookmark.__unicode__() == 'Test Bookmark'


@pytest.mark.django_db
def test_bookmarks_get_edit_url_returns_correct_url():
    user = make_users(1)[0]
    tag = Tag(title='Test Tag', slug='test-tag', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', tag=tag,
             url="http://www.testers.com", user=user).save()
    bookmark = Bookmark.objects.get(pk=1)
    assert bookmark.get_edit_url() == '/bookmarks/edit/test-tag/test-bookmark/'


@pytest.mark.django_db
def test_bookmarks_get_delete_url_returns_correct_url():
    user = make_users(1)[0]
    tag = Tag(title='Test Tag', slug='test-tag', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', tag=tag,
             url="http://www.testers.com", user=user).save()
    bookmark = Bookmark.objects.get(pk=1)
    assert bookmark.get_delete_url() == '/bookmarks/delete/test-tag/test-bookmark/'
