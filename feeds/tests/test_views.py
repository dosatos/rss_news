import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from feeds.views import source_page


@pytest.mark.django_db
class TestViews:

    def test_source_view_authenticated(self):
        path = reverse('sources')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = source_page(request)
        assert response.status_code == 200

    def test_source_view_unauthenticated(self):
        path = reverse('sources')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = source_page(request)
        assert response.status_code == 200

    def test_feeds_view_authenticated(self):
        path = reverse('feeds')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = source_page(request)
        assert response.status_code == 200

    def test_feeds_view_unauthenticated(self):
        path = reverse('feeds')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = source_page(request)
        assert response.status_code == 200

    def test_feeds_view_authenticated(self):
        path = reverse('bookmarks')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = source_page(request)
        assert response.status_code == 200

    def test_feeds_view_unauthenticated(self):
        path = reverse('bookmarks')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = source_page(request)
        assert response.status_code == 301


