import feedparser


def parse(url):
    return feedparser.parse(url)


def get_source(parsed):
    source = parsed['feed']
    print(source['link'])
    return {
        'link': source['link'],
        'title': source['title'],
    }

def get_article(parsed):
    pass