import pytest
from feeds.models import Source
from feeds import utils


@pytest.fixture()
def setup():
    """ initial testing setup """
    url = 'http://www.nu.nl/rss/Algemeen'
    parsed = utils.parse(url)
    source = utils.get_source(parsed)
    return parsed, source


def test_regex_in_parse():
    """
    Validates regular expressions normalize the url.
    """
    url1 = 'www.nu.nl/rss/Algemeen'
    url2 = 'http://www.nu.nl/rss/Algemeen'
    url3 = 'https://www.nu.nl/rss/Algemeen'
    assert utils.parse(url1)['entries'] == utils.parse(url2)['entries'] == utils.parse(url3)['entries']


def test_source_link_title_retrieve(setup):
    """
    Validates get_source() returns title and link correctly

    :param setup: tuple of two objects: parsed and source (from the setup fixture)
    :return: None
    """
    _, source = setup
    assert source['title'] == 'NU - Algemeen' and source['link'] == 'https://www.nu.nl/rss/Algemeen'


@pytest.mark.django_db
def test_get_articles(setup):
    """
    Validates get_articles() returns
        not empty list of articles that are in the form of dict objects

    :param setup: tuple of two objects: parsed and source (from the setup fixture)
    :return: None
    """
    parsed, source_fields = setup
    defaults = {'title': source_fields['title']}
    source = Source.objects.get_or_create(link=source_fields['link'],
                                  defaults=defaults)
    articles = utils.get_articles(parsed, source)
    assert len(articles) >= 0 and type(articles) == list and type(articles[0]) == dict


@pytest.mark.django_db
def test_extend_source():
    """
    Validates the same source could be processed twice:
        No uniqueness conflict
    """
    url = 'http://www.nu.nl/rss/Algemeen'
    for _ in range(2):
        utils.extend_sources(url)