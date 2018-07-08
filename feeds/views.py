from django.shortcuts import render
from feeds.models import Source


def feeds(request):
    pass


def source_page(request):
    template_path = 'feeds/sources.html'
    sources = Source.objects.all()
    context = {'sources': sources}
    return render(request, template_path, context)
