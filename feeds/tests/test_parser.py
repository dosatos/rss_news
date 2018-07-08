import pytest
from feeds.utils import parse, get_source, save_source_to_db, get_articles

@pytest.fixture()
def parsed():
    url = 'http://www.nu.nl/rss/Algemeen'
    parsed = parse(url)
    return parsed

def test_get_source(parsed):
    source = get_source(parsed)
    assert source.title == 'NU - Algemeen' and source.link == 'https://www.nu.nl/algemeen'


def test_get_articles(parsed):
    articles = get_articles(parsed)
    assert articles[0].title != None and type(articles[0].title) == str


@pytest.mark.django_db
def test_save_to_db(parsed):
    url = 'http://www.nu.nl/rss/Algemeen'
    save_source_to_db(url)


# def test_update_source(parsed):
#     get_articles(parsed)
#     update_source()
#     article.save()