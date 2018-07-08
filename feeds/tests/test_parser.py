import pytest
from feeds.utils import parse, get_source, save_source_to_db, get_articles

@pytest.fixture()
def setup():
    url = 'http://www.nu.nl/rss/Algemeen'
    parsed = parse(url)
    source = get_source(parsed)
    return parsed, source

def test_get_source(setup):
    _, source = setup
    assert source.title == 'NU - Algemeen' and source.link == 'https://www.nu.nl/algemeen'


def test_get_articles(setup):
    parsed, source = setup
    articles = get_articles(parsed, source)
    assert articles[0].title != None and type(articles[0].title) == str
