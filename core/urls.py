from django.urls import path

from core import main

urlpatterns = [
    path('', main.home, name='home'),
]