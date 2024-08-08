from django.urls import path

from core import main
from .views import index,search

urlpatterns = [
    path('', main.home, name='home'),
    path('todos/', index, name='index'),
    path('signin/', main.signin, name='signin'),
    path('signin/user/', main.signin, name='user_signin'),
    path('search/', search, name='search'),  # new

    path('settings/', main.app_settings, name='app_settings'),
    path('settings/subjects/', main.subject_page, name='subject_page'),
    path('settings/subjects/<uuid:subject_id>/', main.subject, name='subject'),
    path('settings/subjects/create/', main.subject, name='create_subject'),
]