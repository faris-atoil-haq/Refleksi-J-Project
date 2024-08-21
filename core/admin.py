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

class SubjectReflectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'updated_at', 'created_at',]
    search_fields = ['id', 'subject__id', 'subject__name',]
    date_hierarchy='created_at'
    
class ReflectionQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_reflection', 'order', 'show', 'updated_at', 'created_at',]
    search_fields = ['id', 'subject_reflection__id', 'question']
    date_hierarchy='created_at'
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