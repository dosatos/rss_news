from django.urls import reverse, resolve


class TestUrls:

    def test_feeds_url_exists(self):
        path = reverse('feeds')
        assert resolve(path).view_name == 'feeds'

    def test_source_url_exists(self):
        path = reverse('sources')
        assert resolve(path).view_name == 'sources'

    def test_bookmarks_url_exists(self):
        path = reverse('bookmarks')
        assert resolve(path).view_name == 'bookmarks'

    def test_bookmarks_url_exists(self):
        path = reverse('add-bookmark')
        assert resolve(path).view_name == 'add-bookmark'