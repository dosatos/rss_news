from django.urls import reverse, resolve
# import pytest


class TestUrls:

    def test_feeds_url_exists(self):
        path = reverse('feeds')
        assert resolve(path).view_name == 'feeds'

    def test_feeds_url(self):
        path = reverse('feeds')
        assert resolve(path).view_name == 'feeds'
