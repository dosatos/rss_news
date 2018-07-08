import pytest
from feeds.utils import parse, get_source, get_articles, extend_sources
from feeds.models import Source


@pytest.fixture()
def setup():
    """ initial testing setup """
    url = 'http://www.nu.nl/rss/Algemeen'
    parsed = parse(url)
    source = get_source(parsed)
    return parsed, source


def test_get_source(setup):
    """ this test validates get_source func is working well """
    _, source = setup
    assert source['title'] == 'NU - Algemeen' and source['link'] == 'https://www.nu.nl/rss/Algemeen'


@pytest.mark.django_db
def test_extend_source(setup):
    """ this test checks if the same source could be posted twice """
    url = 'http://www.nu.nl/rss/Algemeen'
    extend_sources(url)
    extend_sources(url)


@pytest.mark.django_db
def test_get_articles(setup):
    """ thistest validates get_articles func is working well """
    parsed, source_fields = setup
    defaults = {'title': source_fields['title']}
    source = Source.objects.get_or_create(link=source_fields['link'],
                                  defaults=defaults)
    articles = get_articles(parsed, source)
    assert articles[0]['title'] != None and type(articles[0]['title']) == str and type(articles[0]) == dict