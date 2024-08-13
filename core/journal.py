import pytz
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET

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
    subjects = TeacherAgenda.objects.filter(
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
    context = {
        'page': 'schedule',
        'page_title': 'Jadwal Pertemuan'
    }
    return render(request, 'core/journal/schedule.html', context)
    
@login_required
@require_GET
def schedule_items(request):
    agenda_list = []
    for i in range(0, 7):
        date = timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).replace(hour=0, minute=0, second=0) + timezone.timedelta(days=i)
        schedules = TeacherAgenda.objects.filter(start_time__date=date.date()).order_by('start_time')
        agenda_list.append({'date': date, 'schedules': schedules})
    print(agenda_list)
    context = {
        'agenda_list': agenda_list,
    }
    return render(request, 'core/journal/schedule-items.html', context)