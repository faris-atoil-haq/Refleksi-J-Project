from django.contrib import admin

from core.models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','updated_at','created_at',]
    search_fields = ['id', 'title']
    date_hierarchy='created_at'
admin.site.register(Article, ArticleAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'updated_at', 'created_at',]
    search_fields = ['id', 'name']
    date_hierarchy='created_at'
admin.site.register(Subject, SubjectAdmin)

class ReflectionQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'order', 'updated_at', 'created_at',]
    search_fields = ['id', 'question']
    order='order'
admin.site.register(ReflectionQuestion, ReflectionQuestionAdmin)

class TeacherAgendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'start_time', 'end_time', 'updated_at', 'created_at',]
    search_fields = ['id', 'user__firstname', 'user__id', 'subject__id']
    date_hierarchy='created_at'
admin.site.register(TeacherAgenda, TeacherAgendaAdmin)

class JournalAdmin(admin.ModelAdmin):
    list_display = ['id', 'agenda', 'question', 'updated_at', 'created_at',]
    search_fields = ['id', 'agenda__id']
    date_hierarchy='created_at'
admin.site.register(Journal, JournalAdmin)

class VerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified', 'code', 'admin', 'instansi', 'created_at']
    search_fields = ['user__username', 'instansi']
    date_hierarchy='created_at'
admin.site.register(Verification, VerificationAdmin)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'module_file', 'created_at', 'updated_at']
    search_fields = ['id', 'user__username', 'module_file__file']
    date_hierarchy='created_at'
admin.site.register(Module, ModuleAdmin)
    
class ModuleAssessmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'module', 'category', 'updated_at', 'created_at']
    search_fields = ['id', 'module__id', 'category']
    date_hierarchy='created_at'
admin.site.register(ModuleAssessment, ModuleAssessmentAdmin)

class AngketQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'target', 'question', 'description', 'order', 'option_range', 'option_step', 'option_start_label', 'option_end_label', 'updated_at', 'created_at']
    search_fields = ['id', 'question']
    date_hierarchy='created_at'
admin.site.register(AngketQuestion, AngketQuestionAdmin)
    
class AngketSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'link', 'accept_response', 'created_at', 'updated_at']
    search_fields = ['id', 'user__id', 'user__email', 'user__firstname', 'user__username']
    date_hierarchy='created_at'
admin.site.register(AngketSession, AngketSessionAdmin)

class AngketResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'respondent', 'question', 'question_text', 'answer', 'answer_options', 'created_at', 'updated_at']
    search_fields = ['id', 'respondent', 'question_text']
    date_hierarchy='created_at'
admin.site.register(AngketResponse, AngketResponseAdmin)