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
def test_list_tags(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    response = client.get('/tags/')
    assert len(response.context['tags']) == 1


@pytest.mark.django_db
def test_view_tag(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    response = client.get('/tags/view/title/')
    assert 'Test Bookmark' in response.content


@pytest.mark.django_db
def test_view_tag_throws_404(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    response = client.get('/tags/view/titleeeee/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_add_tag(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]

    assert client.login(username=user.username, password=password)
    assert client.get('/tags/add/')
    client.post('/tags/add/', data={
        'title': 'Test Tag',
        'user': user,
    }, user=user)
    assert len(Tag.objects.all()) == 1


@pytest.mark.django_db
def test_add_tag_has_invalid_title(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]

    assert client.login(username=user.username, password=password)
    assert client.get('/tags/add/')
    post_response = client.post('/tags/add/', data={
        'title': '',
        'user': user,
    }, user=user)
    assert len(Tag.objects.all()) == 0
    assert ['title'] == post_response.context['form'].errors.keys()


@pytest.mark.django_db
def test_edit_tag(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    assert client.get('/tags/edit/title/')
    client.post('/tags/edit/title/', data={
        'title': 'New Name',
        'user': user,
    }, user=user, slug=tag.slug)
    tag = Tag.objects.get(pk=1)
    assert tag.title == 'New Name'


@pytest.mark.django_db
def test_edit_tag_has_invalid_title(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    assert client.get('/tags/edit/title/')
    post_response = client.post('/tags/edit/title/', data={
        'title': '',
        'user': user,
    }, user=user, slug=tag.slug)
    assert ['title'] == post_response.context['form'].errors.keys()


@pytest.mark.django_db
def test_edit_tag_throws_404(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    response = client.get('/tags/edit/titleeeee/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_tag(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    client.post('/tags/delete/title/', user=user, slug=tag.slug)
    assert len(Tag.objects.all()) == 0


@pytest.mark.django_db
def test_delete_tag_throws_405(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()

    assert client.login(username=user.username, password=password)
    response = client.get('/tags/delete/title/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_delete_tag_deletes_bookmarks_too(client):
    password = 'P@ssw0rd!'
    user = make_users(1)[0]
    tag = Tag(title='title', slug='title', user=user)
    tag.save()
    Bookmark(title='Test Bookmark', slug='test-bookmark', user=user,
             description='', tags=tag, url='http://www.google.com').save()

    assert client.login(username=user.username, password=password)
    client.post('/tags/delete/title/', user=user, slug=tag.slug)
    assert len(Tag.objects.all()) == 0
    assert len(Bookmark.objects.all()) == 0
