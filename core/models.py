import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Verification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_query_name="verification"
    )
    verified = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    instansi = models.CharField(max_length=256, null=True, blank=True)
    code = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Verification for: ' + self.user.first_name



class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.FileField(
        upload_to="refleksi-j-article", null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id} {self.title}'

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_level = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    order = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id} {self.name}'
    
class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="module_file")
    name = models.CharField(max_length=255, blank=True, null=True)
    module_file = models.FileField(
        upload_to="refleksi-j-module", null=True, blank=True)
    chatpdf_id = models.CharField(max_length=255, blank=True, null=True)
    subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

class ReflectionQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField(blank=True, null=True)
    articles = models.ManyToManyField(Article, related_name="reflection_questions")
    order = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id} {self.question}'
    
class AgendaReference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

class TeacherAgenda(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    reference = models.ForeignKey(AgendaReference, blank=True, null=True, on_delete=models.SET_NULL, related_name='agendas')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        if self.subject:
            return f'{self.id} {self.user} {self.subject.name} {self.start_time}'
        return f'{self.id} {self.user}'

class Journal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.SET_NULL)
    subject_text = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    agenda = models.ForeignKey(TeacherAgenda, blank=True, null=True, on_delete=models.CASCADE, related_name='journals')
    question = models.ForeignKey(ReflectionQuestion, blank=True, null=True, on_delete=models.SET_NULL)
    question_text = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True) # jawaban dari pertanyaan refleksi
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id} {self.agenda} {self.question}'
    
class HeadNews(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(blank=True, null=True)
    link_text = models.CharField(blank=True, null=True, max_length=255)
    link_url = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        if self.text:
            return f'{self.id} {self.text[:20]}...'
        else:
            return f'{self.id}'
        
MODULE_ASSESSMENT_CATEGORY = [
    ('komponen_wajib', 'Komponen Wajib'),
    ('penialaian_kesesuaian', 'Penilaian Kesesuaian'),
    ('suggestion', 'Suggestion'),
]

class ModuleAssessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=255, blank=True, null=True, choices=MODULE_ASSESSMENT_CATEGORY)
    module = models.ForeignKey(Module, blank=True, null=True, on_delete=models.CASCADE)
    response = models.TextField(blank=True, null=True)
    response_json = models.JSONField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id} {self.category} {self.module}'
    
ANGKET_TARGET = [
    ('student', 'Student'),
    ('teacher', 'Teacher'),
]

class AngketQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.CharField(max_length=25, blank=True, null=True, choices=ANGKET_TARGET, default='student')
    question = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    option_range = models.IntegerField(null=True, blank=True)
    option_step = models.IntegerField(null=True, blank=True)
    option_start_label = models.CharField(max_length=255, blank=True, null=True)
    option_end_label = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id} {self.order}'

class AngketSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.CharField(max_length=25, blank=True, null=True, choices=ANGKET_TARGET, default='student')
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    link = models.TextField(blank=True, null=True)
    accept_response = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
class AngketResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AngketSession, blank=True, null=True, on_delete=models.CASCADE, related_name="responses")
    respondent = models.CharField(max_length=255, blank=True, null=True)
    question = models.ForeignKey(AngketQuestion, blank=True, null=True, on_delete=models.CASCADE)
    question_text = models.TextField(blank=True, null=True)
    answer = models.IntegerField(blank=True, null=True)
    answer_options = models.JSONField(blank=True, null=True)
    # answer_options format:
    # {"option_range": 3, "option_step": 1, "option_start_label": "Sangat Tidak Puas", "option_end_label": "Sangat Puas"}
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.id} {self.respondent} {self.question}'