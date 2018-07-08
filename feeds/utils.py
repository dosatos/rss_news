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