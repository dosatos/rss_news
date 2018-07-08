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
    return dict(link=parsed['href'], title=source['title'])


def get_articles(parsed, source):
    """ this func returns list of articles """
    entries = parsed['entries']
    amsterdam = timezone('Europe/Amsterdam')  # TODO: make it generic, it assumes all is amsterdam time
    articles = [dict(link=entry['link'],
                     title=entry['title'],
                     body=entry['summary'],  # TODO: truncate <img> tags parsed as a part of the summary
                     source=source,
                     date_published=amsterdam.localize(datetime.fromtimestamp(mktime(entry['published_parsed']))))
                for entry in entries]
    return articles


def extend_sources(url):
    """ this func saves source into db """
    parsed = parse(url)
    # save sources
    source_fields = get_source(parsed)
    defaults = {'title': source_fields['title']}
    # source = Source.objects.get_or_create(link=source_fields['link'], defaults=defaults)
    source, _ = Source.objects.get_or_create(link=parsed['feed']['link'], defaults={'title': parsed['feed']['title']})
    # save articles
    articles = get_articles(parsed, source)
    update_source(articles)


def update_source(articles):
    """ this func saves articles into db """
    for a in articles:
        defaults = {
            'title': a['title'],
            'body': a['body'],
            'source': a['source'],
            'date_published': a['date_published']
        }
        Article.objects.get_or_create(link=a['link'], defaults=defaults)