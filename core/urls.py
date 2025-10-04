from django.urls import path

from core import angket, journal, main, module, public

urlpatterns = [
    path('load_articles/', public.load_articles, name='load_articles'),
    path('article/<uuid:id>/', public.get_article, name='article_page'),
    
    path('confirm/', main.confirm, name='confirm'),
    path('reset_password/', main.reset_password, name='reset_password'),
    path('forgot/', main.reset_password_email, name='reset_password_email'),
    path('signup/', main.signup, name='signup'),
    path('login/', main.signin, name='login'),
    path('logout/', main.signout, name='logout'),
    
    path('angket/<uuid:id>/', angket.public_angket, name='public_angket'),
    path('angket/<uuid:id>/save/', angket.respond_angket, name='respond_angket'),
    path('angket/done/', angket.done_angket, name='done_angket'),

    path('', main.home, name='home'),
    path('modul/', module.module, name='module'),
    path('modul/<uuid:subject>/', module.module, name='module_subject'),
    path('modul/subjects/create/', module.subject_manager, name='create_new_subject'),
    path('modul/upload/', module.upload_module, name='upload_module'),
    path('modul/<uuid:id>/name/', module.module_name, name='module_name'),
    path('modul/<uuid:id>/delete/', module.delete_module, name='delete_module'),
    path('modul/<uuid:id>/upload/ai/', module.upload_to_chatpdf, name='upload_to_chatpdf'),
    path('modul/<uuid:id>/generate/check-component/', module.check_module_components, name='check_module_components'),
    path('modul/<uuid:id>/generate/assessment/', module.generate_module_assessment, name='generate_module_assessment'),
    path('modul/<uuid:id>/generate/suggestion/', module.generate_suggestion, name='generate_suggestion'),
    path('modul/<uuid:id>/feedback/', module.get_feedback, name='get_feedback'),
    path('modul/<uuid:id>/view-feedback-btn/', module.get_view_feedback_btn, name='get_view_feedback_btn'),
    
    path('refleksi/today/', journal.today_agenda, name='today_agenda'),
    path('refleksi/history/', journal.latest_reflection_journals, name='latest_reflection_journals'),
    
    path('jadwal/', journal.schedule, name='schedule'),
    path('jadwal/add/', journal.schedule_subject, name='add_schedule'),
    path('jadwal/<uuid:id>/', journal.schedule_subject, name='edit_schedule'),
    path('jadwal/items/', journal.schedule_items, name='schedule_items'),
    path('jadwal/<uuid:id>/refleksi/', journal.refleksi_input, name='begin_refleksi_input'),
    path('jadwal/<uuid:id>/refleksi/<int:refleksi>/', journal.refleksi_input, name='refleksi_input'),
    path('jadwal/<uuid:id>/refleksi/summary/', journal.summary_refleksi, name='summary_refleksi'),
    path('jadwal/save/', journal.refleksi_input, name='refleksi_input_save'),
    
    path('angket/', angket.main, name='angket'),
    path('angket/generate/', angket.generate_angket, name='generate_angket'),
    path('angket/generate/', angket.generate_angket, name='generate_angket'),
    path('angket/<uuid:id>/delete/', angket.delete_angket, name='delete_angket'),
    path('angket/<uuid:id>/public/', angket.toggle_accept_response, name='toggle_accept_response'),
    path('angket/<uuid:id>/result/', angket.angket_result, name='angket_result'),
    path('angket/<uuid:id>/form/', angket.angket_form, name='angket_form'),
    
    path('profile/', main.user_profile, name='user_profile'),
    
    path('article/', main.article, name='article'),
    
    # Application Settings
    path('settings/', main.app_settings, name='app_settings'),

    path('settings/article/', main.articles_template, name='articles_template'),
    path('settings/article/create/', main.manage_article, name='create_article'),
    path('settings/article/manage/<uuid:id>/', main.manage_article, name='manage_article'),
    path('settings/refleksi/order/', main.order_article, name='order_article'),
    
    path('settings/refleksi/', main.reflection_templates, name='reflection_templates'),
    path('settings/refleksi/create/', main.manage_reflection_question, name='create_reflection_question'),
    path('settings/refleksi/order/', main.order_reflection_question, name='order_reflection_question'),
    path('settings/refleksi/<uuid:id>/', main.manage_reflection_question, name='manage_reflection_question'),
    
    path('settings/angket/', main.angket_templates, name='angket_templates'),
    path('settings/angket/<str:angket_type>/', main.angket_templates, name='angket_templates'),
    path('settings/angket/create/', main.manage_angket_question, name='create_angket_question'),
    path('settings/angket/<str:angket_type>/create/', main.manage_angket_question, name='create_angket_question'),
    path('settings/angket/order/', main.order_angket_question, name='order_angket_question'),
    path('settings/angket/<str:angket_type>/order/', main.order_angket_question, name='order_angket_question'),
    path('settings/angket/<uuid:id>/', main.manage_angket_question, name='manage_angket_question'),
    path('settings/angket/<str:angket_type>/<uuid:id>/', main.manage_angket_question, name='manage_angket_question'),
]