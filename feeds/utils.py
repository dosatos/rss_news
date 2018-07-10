import re
import feedparser
from django.utils import timezone
from datetime import datetime
from time import mktime
from feeds.models import Source, Article


def parse(url):
    """
    Generates an initial parse object to be used
    for getting article and source objects.

    Regular expression is used to validate and correct
    for special cases of the url provided.

    :param url: str
    :return: feedparser.FeedParserDict
    """
    regex = re.compile(
        r'^(?:http)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not re.match(regex, url):
        url = "http://" + url
    return feedparser.parse(url)


def get_source(parsed):
    """
    Generates a dictionary with fields 'title' and 'link'
    from a given "parsed" object.

    :param parsed: feedparser.FeedParserDict
    :return: feeds.models.Source
    """
    source = parsed['feed']
    return {
        'link': parsed['href'], 'title': source['title']
    }


def get_articles(parsed, source):
    """
    From a given parsed object and a source provided,
    generates article dict objects.

    :param parsed: feedparser.FeedParserDict
    :param source: feeds.models.Source
    :return: list of dict objects
    """
    entries = parsed['entries']

    articles = [{'link': entry['link'],
                 'title': entry['title'],
                 'body': entry['summary'],  # TODO: truncate <img> tags parsed as a part of the summary
                 'source': source,
                 'date_published': get_tz_aware_date(entry['published_parsed'])}
                for entry in entries]
    return articles


def extend_sources(url):
    """
    Updates a feed source by the given url to an rss news feed.

    Consists of two parts:
        1. Saves a source object based on the url parsed
        2. Updates articles based on the url parsed and the source from the above

    :param url: str
    :return: None
    """
    parsed = parse(url)

    # Part 1. save sources
    source_fields = get_source(parsed)
    defaults = {'title': source_fields['title']}
    source, _ = Source.objects.get_or_create(link=source_fields['link'], defaults=defaults)

    # Part 2. save articles
    articles = get_articles(parsed, source)
    update_source(articles)


def update_source(articles):
    """
    Updates a feed source by the given list of articles.
    If an article is in the database it is not added any more.
        get_or_create() method is used to ensure the latter.

    :param articles: list of dict objects
    :return: None
    """
    for a in articles:
        defaults = {
            'title': a['title'],
            'body': a['body'],
            'source': a['source'],
            'date_published': get_tz_aware_date(a['date_published'])
        }
        Article.objects.get_or_create(link=a['link'], defaults=defaults)


def get_tz_aware_date(parsed_time):
    """
    Adds time zone to the tz-unaware/naive time objects.
    Default time zone is set.

    :param parsed_time: datetime
                       if time.struct_time is provided, then changed to datetime
    :return: datetime.datetime
    """
    try:
        parsed_time = datetime.fromtimestamp(mktime(parsed_time))
    except TypeError as e:
        # print("Error, conversion attempt error", e)  # to be logged, is printed for simplicity
        pass
    date_published = parsed_time if not timezone.is_naive(parsed_time) else timezone.make_aware(parsed_time)
    return date_published