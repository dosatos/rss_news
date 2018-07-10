from datetime import timedelta
from celery.task import periodic_task

from feeds.models import Source
from feeds import utils

@periodic_task(run_every=timedelta(minutes=15))
def auto_update():
    sources = Source.objects.all()
    urls = [source.link for source in sources]
    for url in urls:
        utils.extend_sources(url)
