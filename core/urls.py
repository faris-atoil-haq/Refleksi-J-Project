from django.urls import path

from core import main

from .views import index, search

urlpatterns = [
    path('', main.home, name='home'),
    
    path('signin/', main.signin, name='signin'),
    path('signin/user/', main.signin, name='user_signin'),
    path('search/', search, name='search'),  # new

    # Application Settings
    path('settings/', main.app_settings, name='app_settings'),
    path('settings/refleksi/', main.reflection_templates, name='reflection_templates'),
    path('settings/refleksi/manage/', main.manage_reflection_template, name='manage_reflection_template'),
    path('settings/refleksi/manage/<uuid:id>/', main.manage_reflection_template, name='manage_reflection_template'),
    path('settings/subjects/', main.subject_page, name='subject_page'),
    path('settings/subjects/<uuid:subject_id>/', main.subject, name='subject'),
    path('settings/subjects/create/', main.subject, name='create_subject'),
]