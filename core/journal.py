import pytz
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from core.models import *


@login_required
@require_GET
def today_agenda(request):
    agenda_list = TeacherAgenda.objects.filter(
        start_time=timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).replace(hour=0, minute=0, second=0)
    ).order_by('start_time')
    context = {
        'agenda_list': agenda_list,
    }
    return render(request, 'core/journal/today-agenda.html', context)

@login_required
@require_GET
def latest_reflection_journals(request):
    schedules = TeacherAgenda.objects.filter(user=request.user,
        start_time=timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).replace(hour=0, minute=0, second=0)
    ).values('subject')
    
    latest_journals = []
    for schedule in schedules:
        subject = schedule.subject
        latest_journal = Journal.objects.filter(subject=subject).latest('created_at')
        latest_journals.append(latest_journal)
    
    # For Testing Faris , comment it out to test on home for refleksi list
    # latest_journals = Journal.objects.all()

    context = {
        'latest_journals': latest_journals
    }
    return render(request, 'core/journal/latest-reflection-journals.html', context)

@login_required
@require_GET
def schedule(request):
    subjects = Subject.objects.filter(
        #class_level=''
        ).order_by('name').values('id', 'name')
    
    context = {
        'page': 'schedule',
        'page_title': 'Jadwal Pertemuan',
        'today': timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')),
        'subjects': subjects,
    }
    return render(request, 'core/journal/schedule.html', context)

@login_required
@require_POST
def schedule_subject(request):
    subject_id = request.POST.get('subject')
    date = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    repetition = request.POST.get('repetition')
    if repetition not in ['no_repetition', 'daily', 'weekly', 'monthly']:
        repetition = 'no_repetition'
    
    # Add TeacherAgenda based on the POST data
    subject = Subject.objects.get(id=subject_id)
    start_time = timezone.datetime.strptime(f'{date} {start_time}+07:00', '%d %B %Y %H:%M%z').astimezone(pytz.UTC)
    print(start_time)
    end_time = timezone.datetime.strptime(f'{date} {end_time}+07:00', '%d %B %Y %H:%M%z').astimezone(pytz.UTC)
    print(end_time)
    if repetition == 'no_repetition':
        TeacherAgenda.objects.create(
            user=request.user,
            subject=subject,
            start_time=start_time,
            end_time=end_time
        )
    # elif repetition == 'daily':
        
    
    return redirect('schedule')
    
@login_required
@require_GET
def schedule_items(request):
    agenda_list = []
    now = timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta'))
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(seconds=1)
    
    schedules = TeacherAgenda.objects.filter(start_time__date__range=(start_of_month, end_of_month)).order_by('start_time')
    refleksi_list = ReflectionQuestion.objects.all()
    for schedule in schedules:
        date = schedule.start_time.date()
        if not any(agenda['date'] == date for agenda in agenda_list):
            agenda_list.append({'date': date, 'schedules': []})
        for agenda in agenda_list:
            if agenda['date'] == date:
                agenda['schedules'].append(schedule)
    
    context = {
        'agenda_list': agenda_list,
        'refleksi_list': refleksi_list,
        'today': timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).date(),
    }
    return render(request, 'core/journal/schedule-items.html', context)


@login_required
def refleksi_input(request,id=None,refleksi=None):
    refleksi_list = ReflectionQuestion.objects.all()

    if request.method == 'GET':
        schedule = TeacherAgenda.objects.get(id=id)
        subject = schedule.subject
        refleksi_quest = ReflectionQuestion.objects.get(order=refleksi)
        jurnal,_ = Journal.objects.get_or_create(subject=subject,agenda=schedule,question=refleksi_quest)
        context = {
            'refleksi_quest': refleksi_quest,
            'refleksi_list': refleksi_list,
            'schedule': schedule,
            'jurnal': jurnal,
            'page': 'schedule',
        }
    else:
        schedule = request.POST.get('schedule',None)
        order = request.POST.get('order',None)
        refleksi_answer = request.POST.get('refleksi_answer',None)

        schedule = TeacherAgenda.objects.get(id=schedule)
        question = ReflectionQuestion.objects.get(order=order)
        subject = schedule.subject
        jurnal,_ = Journal.objects.get_or_create(subject=subject,agenda=schedule,question=question)
        
        jurnal.content = refleksi_answer
        jurnal.question_text = question.question
        jurnal.save()

        try:
            refleksi_quest = ReflectionQuestion.objects.get(order=int(order)+1)
        except:
            print("No more question")
            return redirect('schedule')

        context = {
            'refleksi_quest': refleksi_quest,
            'refleksi_list': refleksi_list,
            'schedule': schedule,
            'page': 'schedule',
        }
    return render(request, 'core/journal/refleksi-list.html', context)

