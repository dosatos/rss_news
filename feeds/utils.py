import feedparser
from feeds.models import Source


def parse(url):
    return feedparser.parse(url)


def get_source(parsed):
    source = parsed['feed']
    return Source(link=source['link'], title=source['title'])


def save_source_to_db(url):
    """ this func saves source into db """
    parsed = parse(url)
    s = get_source(parsed)
    s.save()


def get_article(parsed):
    articles = []
    entries = parsed['entries']
    for entry in entries:
        articles.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'summary': entry['summary'],
            'published': entry['published_parsed'],
        })
    return articles