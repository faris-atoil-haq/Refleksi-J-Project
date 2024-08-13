from core.models import HeadNews


def general_context(request):
    head_news = HeadNews.objects.filter(published=True).first()
    context = {
        'head_news': head_news,
    }
    return context