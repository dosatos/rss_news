from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from feeds.models import Source, Article
from feeds.forms import SourceForm
from comments.models import Comment


from feeds import utils
from feeds import tasks

def feeds(request):
    if request.method == "POST":
        return add_bookmark(request)
    template_path = 'feeds/feeds.html'
    articles = Article.objects.all()
    context = {'articles': articles,
               'top_message': f"About {len(articles)} articles on the web-site",
    }
    return render(request, template_path, context)  # TODO: limit number of items shown, so far shows all feeds without limitation


def source_page(request):
    tasks.auto_update.delay()
    template_path = 'feeds/sources.html'
    sources = Source.objects.all()
    context = {'sources': sources}
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            try:  # try to add to the db
                url = form.cleaned_data['link']
                utils.extend_sources(url)
                return redirect('/sources/')
            except KeyError as e:  # display message if the provided url is not valid
                print("Error: ", e)  # prints for the sake of simplicity. should be logged instead.
                context['form'] = form
                context['message'] = 'Please, provide correct source link'
                return render(request, template_path, context)
    form = SourceForm()
    context['form'] = form
    return render(request, template_path, context)


@login_required
def bookmarks(request):
    if request.method == "POST":
        return add_bookmark(request)
    template_path = 'feeds/feeds.html'
    articles =  request.user.bookmarks.all()
    context = {'articles': articles,
               'top_message': f"You have bookmarked {len(articles)} articles."}
    # TODO: limit number of items shown, so far shows all feeds without limitation
    return render(request, template_path, context)


def add_bookmark(request):
    article = get_object_or_404(Article, pk=int(request.POST['key']))
    if article in request.user.bookmarks.all():  # adding to bookmarks
        request.user.bookmarks.remove(article)
    else:  # removing from bookmarks
        request.user.bookmarks.add(article)
    return redirect(request.path)