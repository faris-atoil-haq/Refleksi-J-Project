from django.urls import path

from core import angket, journal, main, module, public

urlpatterns = [
    path('', public.main, name='public'),
    
    path('confirm/', main.confirm, name='confirm'),
    path('reset_password/', main.reset_password, name='reset_password'),
    path('forgot/', main.reset_password_email, name='reset_password_email'),
    path('signup/', main.signup, name='signup'),
    path('login/', main.signin, name='login'),
    path('logout/', main.signout, name='logout'),
    
    path('angket/<uuid:id>/', angket.public_angket, name='public_angket'),
    path('angket/<uuid:id>/save/', angket.respond_angket, name='respond_angket'),
    path('angket/done/', angket.done_angket, name='done_angket'),

    path('app/', main.home, name='home'),
    path('app/modul/', module.module, name='module'),
    path('app/modul/<uuid:subject>/', module.module, name='module_subject'),
    path('app/modul/subjects/create/', module.subject_manager, name='create_new_subject'),
    path('app/modul/upload/', module.upload_module, name='upload_module'),
    path('app/modul/<uuid:id>/delete/', module.delete_module, name='delete_module'),
    path('app/modul/<uuid:id>/upload/ai/', module.upload_to_chatpdf, name='upload_to_chatpdf'),
    path('app/modul/<uuid:id>/generate/check-component/', module.check_module_components, name='check_module_components'),
    path('app/modul/<uuid:id>/generate/assessment/', module.generate_module_assessment, name='generate_module_assessment'),
    path('app/modul/<uuid:id>/generate/suggestion/', module.generate_suggestion, name='generate_suggestion'),
    path('app/modul/<uuid:id>/feedback/', module.get_feedback, name='get_feedback'),
    path('app/modul/<uuid:id>/view-feedback-btn/', module.get_view_feedback_btn, name='get_view_feedback_btn'),
    
    path('app/refleksi/today/', journal.today_agenda, name='today_agenda'),
    path('app/refleksi/history/', journal.latest_reflection_journals, name='latest_reflection_journals'),
    
    path('app/jadwal/', journal.schedule, name='schedule'),
    path('app/jadwal/add/', journal.schedule_subject, name='add_schedule'),
    path('app/jadwal/<uuid:id>/', journal.schedule_subject, name='edit_schedule'),
    path('app/jadwal/items/', journal.schedule_items, name='schedule_items'),
    path('app/jadwal/<uuid:id>/refleksi/', journal.refleksi_input, name='begin_refleksi_input'),
    path('app/jadwal/<uuid:id>/refleksi/<int:refleksi>/', journal.refleksi_input, name='refleksi_input'),
    path('app/jadwal/<uuid:id>/refleksi/summary/', journal.summary_refleksi, name='summary_refleksi'),
    path('app/jadwal/save/', journal.refleksi_input, name='refleksi_input_save'),
    
    path('app/angket/', angket.main, name='angket'),
    path('app/angket/generate/', angket.generate_angket, name='generate_angket'),
    path('app/angket/generate/', angket.generate_angket, name='generate_angket'),
    path('app/angket/<uuid:id>/delete/', angket.delete_angket, name='delete_angket'),
    path('app/angket/<uuid:id>/public/', angket.toggle_accept_response, name='toggle_accept_response'),
    path('app/angket/<uuid:id>/result/', angket.angket_result, name='angket_result'),
    path('app/angket/<uuid:id>/form/', angket.angket_form, name='angket_form'),
    
    path('app/profile/', main.user_profile, name='user_profile'),
    
    # Application Settings
    path('app/settings/', main.app_settings, name='app_settings'),

    path('app/settings/refleksi/', main.reflection_templates, name='reflection_templates'),
    path('app/settings/refleksi/create/', main.manage_reflection_question, name='create_reflection_question'),
    path('app/settings/refleksi/order/', main.order_reflection_question, name='order_reflection_question'),
    path('app/settings/refleksi/<uuid:id>/', main.manage_reflection_question, name='manage_reflection_question'),
    
    path('app/settings/angket/', main.angket_templates, name='angket_templates'),
    path('app/settings/angket/create/', main.manage_angket_question, name='create_angket_question'),
    path('app/settings/angket/order/', main.order_angket_question, name='order_angket_question'),
    path('app/settings/angket/<uuid:id>/', main.manage_angket_question, name='manage_angket_question'),
]