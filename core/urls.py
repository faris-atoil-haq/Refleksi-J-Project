from django.urls import path

from core import main, public

urlpatterns = [
    path('', public.main, name='public'),
    
    path('signin/', main.signin, name='signin'),
    path('signin/user/', main.signin, name='user_signin'),

    path('app/', main.home, name='home'),
    
    # Application Settings
    path('app/settings/', main.app_settings, name='app_settings'),
    path('app/settings/refleksi/', main.reflection_templates, name='reflection_templates'),
    path('app/settings/refleksi/manage/', main.manage_reflection_template, name='manage_reflection_template'),
    path('app/settings/refleksi/manage/<uuid:id>/', main.manage_reflection_template, name='manage_reflection_template'),
    path('app/settings/subjects/', main.subject_page, name='subject_page'),
    path('app/settings/subjects/<uuid:subject_id>/', main.subject, name='subject'),
    path('app/settings/subjects/create/', main.subject, name='create_subject'),
]