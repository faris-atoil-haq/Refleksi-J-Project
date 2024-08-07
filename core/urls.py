from django.urls import path

from core import main
from .views import index,search

urlpatterns = [
    path('', main.home, name='home'),
    path('todos/', index, name='index'),
    path('search/', search, name='search'),  # new
]