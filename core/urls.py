from django.urls import path

from core import main

urlpatterns = [
    path('', main.home, name='home'),
    path('settings/', main.app_settings, name='app_settings'),
    path('settings/subjects/', main.subject_page, name='subject_page'),
    path('settings/subjects/<uuid:subject_id>/', main.subject, name='subject'),
    path('settings/subjects/create/', main.subject, name='create_subject'),
]