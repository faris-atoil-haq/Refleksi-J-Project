import pytz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
    context = {
        'page': 'schedule',
        'page_title': 'Jadwal Pertemuan',
        'today': timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')),
    }
    return render(request, 'core/journal/schedule.html', context)

@login_required
def schedule_subject(request, id=None):
    if request.method == 'GET':
        try:
            agenda = TeacherAgenda.objects.get(id=id, user=request.user)
        except TeacherAgenda.DoesNotExist:
            return HttpResponse(status=404)
        
        context = {
            'agenda': agenda,
        }
        print(context)
        return render(request, 'core/journal/schedule-drawer.html', context)
    
    subject_name = request.POST.get('subject')
    date = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    repetition = request.POST.get('repetition')
    
    if not (subject_name and date and start_time and end_time and repetition):
        return HttpResponse(status=400)
    
    if repetition not in ['no_repetition', 'daily', 'weekly', 'monthly']:
        repetition = 'no_repetition'
    
    # Add TeacherAgenda based on the POST data
    subject, _ = Subject.objects.get_or_create(name=subject_name, user=request.user)
    start_time = timezone.datetime.strptime(f'{date} {start_time}+07:00', '%d %B %Y %H:%M%z').astimezone(pytz.UTC)
    print(start_time)
    end_time = timezone.datetime.strptime(f'{date} {end_time}+07:00', '%d %B %Y %H:%M%z').astimezone(pytz.UTC)
    print(end_time)
    if repetition == 'no_repetition':
        if id:
            TeacherAgenda.objects.filter(id=id, user=request.user).update(
                subject=subject,
                start_time=start_time,
                end_time=end_time
            )
        else:
            TeacherAgenda.objects.create(
                user=request.user,
                subject=subject,
                start_time=start_time,
                end_time=end_time
            )
    # elif repetition == 'daily':
    # elif repetition == 'weekly':
    # elif repetition == 'monthly':
    
    return redirect('schedule')
    
@login_required
@require_GET
def schedule_items(request):
    agenda_list = []
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    month = request.GET.get('month')
    q = request.GET.get('q', '')
    
    today = None
    nearest_today_agenda = None
    init_flowbite = False
    if start_date and end_date:
        start_of_month = timezone.datetime.strptime(start_date, '%m/%d/%Y').replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
        end_of_month = timezone.datetime.strptime(end_date, '%m/%d/%Y').replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
        if start_of_month <= timezone.now() <= end_of_month:
            today = timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).date()
        init_flowbite = True
    elif month:
        month_date = timezone.datetime.strptime(month, '%B %Y')
        start_of_month = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
        end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(seconds=1)
        if start_of_month <= timezone.now() <= end_of_month:
            today = timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).date()
        init_flowbite = True
    else:
        now = timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta'))
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(seconds=1)
        print(end_of_month)
        
        today = timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).date()
    
    conditions = {
        'user':request.user, 
        'start_time__date__range':(start_of_month, end_of_month),
    }
    if q or q != '':
        conditions['subject__name__icontains'] = q
    print(conditions)
    schedules = TeacherAgenda.objects.filter(**conditions).order_by('start_time')
    for schedule in schedules:
        print(schedule.start_time)
        date = schedule.start_time.date()
        if not any(agenda['date'] == date for agenda in agenda_list):
            agenda_list.append({'date': date, 'schedules': []})
        for agenda in agenda_list:
            if agenda['date'] == date:
                agenda['schedules'].append(schedule)
    
    # get agenda['date'] that is the most nearest to today
    if today:
        nearest_today_agenda = min(agenda_list, key=lambda x: abs(x['date'] - today))
    
    context = {
        'agenda_list': agenda_list,
        'nearest_today_agenda': nearest_today_agenda,
        'today': today,
        'init_flowbite': init_flowbite,
    }
    return render(request, 'core/journal/schedule-items.html', context)