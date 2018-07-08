import pytest
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestModels:

    def test_source_add(self):
        source = mixer.blend('feeds.Source', title='NU - Algemeen')
        assert source.title == 'NU - Algemeen'

    def test_article_add(self):
        source = mixer.blend('feeds.Article', title='Hello World', body='Testing summary')
        assert source.title == 'Hello World' and source.body == 'Testing summary'