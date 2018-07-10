import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser

from feeds.views import source_page
from accounts.models import CustomUser


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def guest():
    """
    Returns an unauthorised user 
    :return: django.test.Client
    """
    return Client()


@pytest.fixture
def user(guest):
    """
    Returns an authorised user
    :return: django.test.Client
    """
    username = "user1"
    password = "bar"
    email = "hello@goo.com"
    CustomUser.objects.create_user(username=username, password=password, email=email)
    guest.login(username=username, password=password)
    user = guest
    return user


def test_source_view_unauthenticated(guest):
    response = guest.get('/sources/')
    assert response.status_code == 200


def test_source_view_authenticated(user):
    response = user.get('/sources/')
    assert response.status_code == 200


def test_feeds_view_unauthenticated(guest):
    response = guest.get('/')
    assert response.status_code == 200


def test_feeds_view_authenticated(user):
    response = user.get('/')
    assert response.status_code == 200


def test_feeds_view_unauthenticated(guest):
    response = guest.get('/bookmarks/')
    assert response.status_code == 302
