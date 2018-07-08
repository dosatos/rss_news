import re
import feedparser
from pytz import timezone
from datetime import datetime
from time import mktime
from feeds.models import Source, Article



def parse(url):
    """ this func parses an rss page """
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
    """ this func returns an object of type Source, given the 'parse' from an rss """
    source = parsed['feed']
    return Source(link=source['link'], title=source['title'])


def extend_sources(url):
    """ this func saves source into db """
    parsed = parse(url)
    # save sources
    source = get_source(parsed)  # TODO: it does not check for unique sources yet.
    source.save()
    # save articles
    articles = get_articles(parsed, source)
    update_source(articles)


def get_articles(parsed, source):
    """ this func returns list of articles """
    entries = parsed['entries']
    amsterdam = timezone('Europe/Amsterdam')
    articles = [dict(link=entry['link'],
                     title=entry['title'],
                     body=entry['summary'],
                     source=source,
                     date_published=amsterdam.localize(datetime.fromtimestamp(mktime(entry['published_parsed']))))
                for entry in entries]
    return articles


def update_source(articles):
    """ this func saves articles into db """
    for a in articles:
        defaults = {
            'title': a['title'],
            'body': a['body'],
            'source': a['source'],
            'date_published': a['date_published']
        }
        Article.objects.get_or_create(link=a['link'],
                                      defaults=defaults)
