from django.test import RequestFactory
from django.urls import reverse, resolve
from feeds.views import sources

class TestViews:

    def test_source_view(self):
        path = reverse('sources')
        request = RequestFactory().get(path)
        response = sources(request)
        assert response.status_code == 200
