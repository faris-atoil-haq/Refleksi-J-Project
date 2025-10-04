from django.shortcuts import redirect, render
from django.urls import reverse
import logging as logging

logger = logging.getLogger(__name__)


def handle_400(request, exception):
    return render(request, 'error-handler.html', {'error_code': '400'}, status=400)

def handle_404(request, exception):
    return render(request, 'error-handler.html', {'error_code': '404'}, status=404)

def handle_500(request):
    return render(request, 'error-handler.html', {'error_code': '500'}, status=500)
