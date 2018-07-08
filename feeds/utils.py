import feedparser
import re
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
    """ this func returns an object of type Source, given the 'parse' """
    source = parsed['feed']
    return Source(link=source['link'], title=source['title'])


def save_source_to_db(url):
    """ this func saves source into db """
    parsed = parse(url)
    # save sources
    source = get_source(parsed)
    source.save()
    # save articles
    articles = get_articles(parsed, source)
    update_source(articles)


def get_articles(parsed, source):
    """ this func returns list of articles """
    articles = []
    entries = parsed['entries']
    for entry in entries:
        articles.append(
            Article(
                link=entry['link'],
                title=entry['title'],
                body=entry['summary'],
                source=source,
                guid=entry['id'],
                date_published=entry['published_parsed']
            )
        )
    return articles

def update_source(articles):
    """ this func saves articles into db """
    for a in articles:
        a.save()
