# from datetime import datetime
import pytest
from mixer.backend.django import mixer
from feeds.utils import parse, get_source


@pytest.mark.django_db
class TestModels:

    def test_source_add(self):
        source = mixer.blend('feeds.Source', title='NU - Algemeen')
        assert source.title == 'NU - Algemeen'

    def test_article_add(self):
        source = mixer.blend('feeds.Source', title='Hello World', body='Testing summary')
        assert source.title == 'Hello World'