import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect

from articles import models


def index(request):
    articles = models.Article.objects.filter(is_deleted=False)
    categories = models.Category.objects.filter(parent__isnull=True).order_by('name')
    return render(request, 'articles/base.html',
                  {'categories': categories,
                   'articles': articles})


def article_by_name(request, article_name):
    now = datetime.datetime.now()
    return render(request, 'articles/article_by_name.html',
                  {'name': article_name,
                   'len': len(article_name),
                   'rendered': now})


def article_by_id(request, article_id):
    try:
        article = models.Article.objects.get(id=article_id)
    except (models.Article.DoesNotExist, models.Article.MultipleObjectsReturned):
        return redirect('/')
    return render(request, 'articles/article_by_id.html', {'article': article})


def search(request):
    # Get request value
    # Filter articles
    # Render page
    search = request.GET.get('search', '')
    articles = models.Article.objects.filter(text__icontains=search)
    return render(request, 'articles/search_result.html', {'articles': articles,
                                                           'search': search})


def like_article(request, article_id):
    # Dont scare this. It was just complicated example. lol
    article = models.Article.objects.get(id=article_id)
    if request.method == 'POST':
        article.add_like(request.user)
    return JsonResponse(dict(count=article.likes_set.count()))
    # return redirect(reverse('article_by_id', kwargs={"article_id": article_id}))
