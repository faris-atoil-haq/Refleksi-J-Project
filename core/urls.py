from django.urls import path

from core import journal, main, public

urlpatterns = [
    path('', public.main, name='public'),
    
    path('confirm_signup/', main.confirm_signup, name='confirm_signup'),
    path('signup/', main.signup, name='signup'),
    path('login/', main.signin, name='login'),
    path('logout/', main.signout, name='logout'),

    path('app/', main.home, name='home'),
    path('app/module/', main.module, name='module'),
    path('app/module/upload/', main.upload_module, name='upload_module'),
    path('app/refleksi/today/', journal.today_agenda, name='today_agenda'),
    path('app/refleksi/history/', journal.latest_reflection_journals, name='latest_reflection_journals'),
    path('app/jadwal/', journal.schedule, name='schedule'),
    path('app/jadwal/items/', journal.schedule_items, name='schedule_items'),
    
    # Application Settings
    path('app/settings/', main.app_settings, name='app_settings'),
    path('app/settings/refleksi/', main.reflection_templates, name='reflection_templates'),
    path('app/settings/refleksi/manage/', main.manage_reflection_template, name='manage_reflection_template'),
    path('app/settings/refleksi/manage/<uuid:id>/', main.manage_reflection_template, name='manage_reflection_template'),
    path('app/settings/subjects/', main.subject_page, name='subject_page'),
    path('app/settings/subjects/<uuid:subject_id>/', main.subject, name='subject'),
    path('app/settings/subjects/create/', main.subject, name='create_subject'),
]