from django.shortcuts import render
from feeds.models import Source, Article
from feeds.forms import SourceForm

from feeds import utils


def feeds(request):
    template_path = 'feeds/feeds.html'
    articles = Article.objects.all()
    context = {'feeds': articles}
    return render(request, template_path, context)


def source_page(request):
    template_path = 'feeds/sources.html'
    sources = Source.objects.all()
    context = {'sources': sources}
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            try:
                url = form.cleaned_data['link']
                save_source_to_db(url)
            except KeyError as e:
                print("Error: ", e)  # prints for the sake of simplicity. should be logged instead.
                context['message'] = 'Please, provide correct source link'
                return render(request, template_path, context)
            return redirect('/sources/')
    form = SourceForm()
    context['form'] = form

    return render(request, template_path, context)