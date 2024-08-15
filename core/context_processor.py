from django.conf import settings

from core.models import HeadNews


def general_context(request):
    STAGING = settings.STAGING
    PROD = settings.STAGING
    head_news = HeadNews.objects.filter(published=True).first()
    context = {
        'STAGING': STAGING,
        'PROD': PROD,
        'head_news': head_news,
    }
    return context