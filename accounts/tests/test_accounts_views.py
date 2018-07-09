import pytest
from mixer.backend.django import mixer
from django.test import RequestFactory
from django.urls import reverse
# from django.contrib.auth.models import User, AnonymousUser
from feeds.views import source_page
from accounts.models import CustomUser

@pytest.mark.django_db
class TestViews:

    def test_source_view_authenticated(self):
        path = reverse('login')
        request = RequestFactory().get(path)
        request.user = mixer.blend(CustomUser)
        response = source_page(request)
        assert response.status_code == 200