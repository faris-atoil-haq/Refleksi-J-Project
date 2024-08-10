from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from core.models import Article


def main(request):
    context = {
        'articles': Article.objects.all().order_by('-created_at'),
        'main_public': True,
    }
    return render(request, 'public.html', context)