from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from core.models import Article


def main(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {
        'main_public': True,
    }
    return render(request, 'public.html', context)

def load_articles(request):
    context = {
        'articles': Article.objects.all().order_by("order"),
        'main_public': True,
    }
    return render(request, 'core/settings/article/public-article-display-list.html', context)

def get_article(request,id):
    article = Article.objects.filter(id=id)

    if article:
        article = article.first()
    else:
        return redirect('home')

    context = {
        'id': article.id,
        'title' : article.title,
        'content' : article.content,
        'cover_image' : article.cover_image if article.cover_image else None,
        'main_public': True,
    }
    return render(request, 'core/settings/article/public-article-display-page.html', context)