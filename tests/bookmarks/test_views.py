import datetime

from django.contrib.auth.models import User

import pytest

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
def test_list_bookmarks(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tag=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    response = client.get('/bookmarks/')
    assert len(response.context['bookmarks']) == 1


@pytest.mark.django_db
def test_add_bookmark(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    assert client.get('/bookmarks/add/')
    post_response = client.post('/bookmarks/add/', data={
        'title': 'Test Title',
        'user': user,
        'tag': tag.pk,
        'url': 'http://www.google.com',
    }, user=user)
    assert post_response.status_code == 302
    assert len(Bookmark.objects.all()) == 1


@pytest.mark.django_db
def test_add_bookmark_has_invalid_data(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    assert client.get('/bookmarks/add/')
    post_response = client.post('/bookmarks/add/', data={
        'title': 'Test Title',
        'user': user,
        'tag': tag.pk,
        'url': 'blah',
    }, user=user)
    assert len(Bookmark.objects.all()) == 0
    assert ['url'] == post_response.context['form'].errors.keys()


@pytest.mark.django_db
def test_edit_bookmark(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tag=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    assert client.get('/bookmarks/edit/title/test-bookmark/')
    post_response = client.post('/bookmarks/edit/title/test-bookmark/', data={
        'title': 'Test Title',
        'user': user,
        'tag': tag.pk,
        'url': 'http://www.google.com',
    }, user=user, slug='test-bookmark', tag_slug='title')
    assert post_response.status_code == 302
    assert Bookmark.objects.get(pk=1).title == 'Test Title'


@pytest.mark.django_db
def test_edit_bookmark_has_invalid_data(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tag=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    assert client.get('/bookmarks/edit/title/test-bookmark/')
    post_response = client.post('/bookmarks/edit/title/test-bookmark/', data={
        'title': 'Test Title',
        'user': user,
        'tag': tag.pk,
        'url': 'blah',
    }, user=user, slug='test-bookmark', tag_slug='title')
    assert ['url'] == post_response.context['form'].errors.keys()


@pytest.mark.django_db
def test_edit_bookmark_has_bookmark_that_doesnt_exist(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tag=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    response = client.get('/bookmarks/edit/titleeeee/test-bookmark/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_bookmark(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tag=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    assert client.get('/bookmarks/delete/title/test-bookmark/')
    client.post('/bookmarks/delete/title/test-bookmark/', user=user,
                slug='test-bookmark', tag_slug='title')
    assert len(Bookmark.objects.all()) == 0
