from django.conf import settings
from django.utils import timezone

from core.models import HeadNews


def general_context(request):
    STAGING = settings.STAGING
    PROD = settings.STAGING
    HOST = settings.PARENT_HOST
    head_news = HeadNews.objects.filter(published=True).first()
    context = {
        'STAGING': STAGING,
        'PROD': PROD,
        'HOST': HOST,
        'head_news': head_news,
        'now': timezone.now()
    }
    return context