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
    if request.user.is_authenticated:
        return redirect('home')
    context = {
        'articles': Article.objects.all().order_by("-created_at"),
        'main_public': True,
    }
    return render(request, 'core/settings/article/article-display-list.html', context)

def get_article(request,id):
    if request.user.is_authenticated:
        return redirect('home')
    
    article = Article.objects.filter(id=id)

    if article:
        article = article.first()
    else:
        return redirect('home')

    context = {
        'id': article.id,
        'title' : article.title,
        'content' : article.content,
        'cover_image' : article.cover_image,
        'main_public': True,
    }
    return render(request, 'core/settings/article/article-display-page.html', context)