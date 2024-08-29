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
    subjects = TeacherAgenda.objects.filter(user=request.user,
        start_time=timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).replace(hour=0, minute=0, second=0)
    ).values('subject')
    
    latest_journals = []
    for subject in subjects:
        latest_journal = Journal.objects.filter(subject=subject['subject']).latest('created_at')
        latest_journals.append(latest_journal)

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
    for schedule in schedules:
        date = schedule.start_time.date()
        if not any(agenda['date'] == date for agenda in agenda_list):
            agenda_list.append({'date': date, 'schedules': []})
        for agenda in agenda_list:
            if agenda['date'] == date:
                agenda['schedules'].append(schedule)
    
    context = {
        'agenda_list': agenda_list,
        'today': timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).date(),
    }
    return render(request, 'core/journal/schedule-items.html', context)