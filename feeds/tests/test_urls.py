from django.urls import reverse, resolve


def test_feeds_url_exists():
    path = reverse('feeds')
    assert resolve(path).view_name == 'feeds'


def test_source_url_exists():
    path = reverse('sources')
    assert resolve(path).view_name == 'sources'


def test_bookmarks_url_exists():
    path = reverse('bookmarks')
    assert resolve(path).view_name == 'bookmarks'