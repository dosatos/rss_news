from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from feeds.models import Source, Article
from feeds.forms import SourceForm

from comments.models import Comment
# from comments.forms import CommentForm


from feeds import utils
from feeds import tasks


def feeds(request):
    """
    Generates feeds view
    :param request: django.http.request
    :return: renders a page
    """
    template_path = 'feeds/feeds.html'
    articles = Article.objects.all()
    context = {'articles': articles,
               'top_message': "About {count} articles on the web-site".format(count=len(articles)),
    }
    return render(request, template_path, context)  # TODO: limit number of items shown, so far shows all feeds without limitation


def source_page(request):
    """
    Generates view for a source page
    :param request: django.http.request
    :return: renders a page
    """
    tasks.auto_update.delay()
    template_path = 'feeds/sources.html'
    sources = Source.objects.all()
    context = {'sources': sources}
    if request.method == 'POST':
        return add_source(request, template_path, context)
    form = SourceForm()
    context['form'] = form
    return render(request, template_path, context)


@login_required
def bookmarks(request):
    """
    Generates bookmarks view
    :param request: django.http.request
    :return: renders a page
    """
    template_path = 'feeds/feeds.html'
    articles =  request.user.bookmarks.all()
    context = {'articles': articles,
               'top_message': "You have bookmarked {count} articles.".format(count=len(articles))}
    # TODO: limit number of items shown, so far shows all feeds without limitation
    return render(request, template_path, context)


def add_source(request, template_path, context):
    """
    Adds a new source to the db with the consequent update of the articles table.
        Url is validated for having rss feeds.

    :param request: django.http.request
    :param template_path: str
    :param context: dict
    :return: redirects back if success, otherwise renders the page back with the comments.
    """
    form = SourceForm(request.POST)
    if form.is_valid():
        try:  # try to add to the db
            url = form.cleaned_data['link']
            utils.extend_sources(url)
            return render(request, template_path, context)
        except KeyError as e:  # display message if the provided url is not valid
            print("Error, url provided is not valid: ", e)  # prints for the sake of simplicity. should be logged instead.
            context['form'] = form
            context['message'] = 'Please, provide correct source link'
    return render(request, template_path, context)


def add_bookmark(request):
    """
    Adds/Removes a bookmark to an authorized user.

    :param request: django.http.request
    :return: redirects to '/bookmarks/'
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            article = get_object_or_404(Article, pk=int(request.POST['key']))
            if article in request.user.bookmarks.all():  # adding to bookmarks
                request.user.bookmarks.remove(article)
            else:  # removing from bookmarks
                request.user.bookmarks.add(article)
    return redirect('/bookmarks/')


def add_comment(request):
    """
    Adds commentaries under a particular post.

    :param request: django.http.request
    :return: redirects to '/'
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            author = request.user
            article = get_object_or_404(Article, pk=int(request.POST['articleID']))
            content = request.POST['content']
            Comment.objects.create(author=author, article=article, content=content)
    return redirect('/')