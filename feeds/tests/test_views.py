import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory
from django.urls import reverse, resolve
from django.contrib.auth.models import User, AnonymousUser
from feeds.views import sources


@pytest.mark.django_db
class TestViews:

    def test_source_view_authenticated(self):
        path = reverse('sources')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = sources(request)
        assert response.status_code == 200

    def test_source_view_unauthenticated(self):
        path = reverse('sources')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = sources(request)
        assert response.status_code == 200

    # def test_source_template_added(self):
    #     path = reverse('sources')
    #     request = RequestFactory().get(path)
    #     response = sources(request)
    #     assert 'source.html' in [t.name for t in response.templates]

