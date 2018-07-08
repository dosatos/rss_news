from django.shortcuts import render
from feeds.models import Source, Article


def feeds(request):
    template_path = 'feeds/feeds.html'
    articles = Article.objects.all()
    context = {'feeds': articles}
    return render(request, template_path, context)


def source_page(request):
    template_path = 'feeds/sources.html'
    sources = Source.objects.all()
    context = {'sources': sources}
    return render(request, template_path, context)
