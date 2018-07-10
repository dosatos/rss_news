import pytest
from mixer.backend.django import mixer
from feeds.models import Article


@pytest.mark.django_db
class TestModels:

    def test_source_add(self):
        """ this test validates a source model is created well """
        source = mixer.blend('feeds.Source', title='NU - Algemeen')
        assert source.title == 'NU - Algemeen'

    def test_article_add(self):
        """ this test validates an article model is created well """
        article = mixer.blend('feeds.Article', title='Hello World', body='Testing summary')
        assert article.title == 'Hello World' and article.body == 'Testing summary'

    def test_bookmarking(self):
        """ this test validates many to many relation ship works well """
        articles = mixer.cycle(3).blend(Article)
        user = mixer.blend('accounts.CustomUser', bookmarks=articles)
        assert user.bookmarks.count() == 3
