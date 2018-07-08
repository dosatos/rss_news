import pytest
from feeds.utils import parse, get_source, get_article

@pytest.fixture()
def parsed():
    url = 'http://www.nu.nl/rss/Algemeen'
    parsed = parse(url)
    return parsed

def test_get_source(parsed):
    source = get_source(parsed)
    assert source.title == 'NU - Algemeen' and source.link == 'https://www.nu.nl/algemeen'


def test_get_article(parsed):
    articles = get_article(parsed)
    assert articles[0]['title'] != None