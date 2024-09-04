from datetime import timedelta

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
        user=request.user,
        start_time__date=timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).replace(hour=0, minute=0, second=0).date()
    ).order_by('start_time')
    context = {
        'agenda_list': agenda_list,
    }
    return render(request, 'core/journal/today-agenda.html', context)

@login_required
@require_GET
def latest_reflection_journals(request):
    schedules = TeacherAgenda.objects.filter(
        user=request.user,
        start_time__date=timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).replace(hour=0, minute=0, second=0).date()
    ).order_by('start_time')
    
    latest_journals = []
    for schedule in schedules:
        subject = schedule.subject
        journals = Journal.objects.filter(
            subject=subject, 
            agenda__start_time__date__lt=timezone.localtime(timezone.now(), timezone=pytz.timezone('Asia/Jakarta')).date())
        if journals:
            latest_journals.append(journals.latest('created_at'))
    
    # For Testing Faris , comment it out to test on home for refleksi list
    # latest_journals = Journal.objects.all()

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
    
    # POST
    subject_name = request.POST.get('subject')
    date = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    repetition = request.POST.get('repetition')
    apply_changes_to = request.POST.get('apply_changes_to')
    delete = request.POST.get('delete')
    print(request.POST)
    
    if not delete:
        if not (subject_name and date and start_time and end_time):
            return HttpResponse(status=400)
        if not id and not repetition:
            return HttpResponse(status=400)
        if id and not apply_changes_to:
            return HttpResponse(status=400)
    elif not id:
        return HttpResponse(status=400)
    
    if repetition and repetition not in ['no_repetition', 'daily', 'weekly']:
        repetition = 'no_repetition'
    
    if apply_changes_to and apply_changes_to not in ['this', 'related']:
        apply_changes_to = 'this'
    
    if delete:
        try:
            agenda = TeacherAgenda.objects.get(id=id, user=request.user)
        except:
            return redirect('schedule')
        
        if apply_changes_to == 'related':
            try:
                TeacherAgenda.objects.filter(reference=agenda.reference, start_time__gt=timezone.now()).delete()
            except Exception as e:
                print(e)
        
        agenda.delete()
        return redirect('schedule')
        
    # Add TeacherAgenda based on the POST data
    subject, _ = Subject.objects.get_or_create(name=subject_name, user=request.user)
    start_time = timezone.datetime.strptime(f'{date} {start_time}+07:00', '%d %B %Y %H:%M%z').astimezone(pytz.UTC)
    print(start_time)
    end_time = timezone.datetime.strptime(f'{date} {end_time}+07:00', '%d %B %Y %H:%M%z').astimezone(pytz.UTC)
    print(end_time)
    if repetition == 'no_repetition':
        main_agenda = TeacherAgenda.objects.create(
            user=request.user,
            subject=subject,
            start_time=start_time,
            end_time=end_time
        )
    elif repetition == 'daily':
        reference = AgendaReference.objects.create()
        main_agenda = TeacherAgenda.objects.create(
            user=request.user,
            subject=subject,
            start_time=start_time,
            end_time=end_time,
            reference=reference
        )
        
        now = timezone.now()
        next_month = (now+timedelta(days=32-now.day)).replace(day=1)
        next_two_month = (next_month+timedelta(days=32)).replace(day=1)
        next_three_month = (next_two_month+timedelta(days=32)).astimezone(pytz.timezone('Asia/Jakarta')).replace(day=now.day, hour=start_time.hour, minute=start_time.minute)
        for i in range(1, 91):
            if main_agenda.start_time + timezone.timedelta(days=i) > next_three_month:
                break
            
            day_name = (main_agenda.start_time + timezone.timedelta(days=i)).strftime('%A')
            print(day_name)
            if day_name.lower() in ['saturday', 'sunday']:
                continue
            
            next_start_time = main_agenda.start_time + timezone.timedelta(days=i)
            next_end_time = main_agenda.end_time + timezone.timedelta(days=i)
            
            TeacherAgenda.objects.create(
                user=request.user,
                subject=subject,
                start_time=next_start_time,
                end_time=next_end_time,
                reference=reference
            )
    elif repetition == 'weekly':
        reference = AgendaReference.objects.create()
        main_agenda = TeacherAgenda.objects.create(
            user=request.user,
            subject=subject,
            start_time=start_time,
            end_time=end_time,
            reference=reference
        )
        
        now = timezone.now()
        next_month = (now+timedelta(days=32-now.day)).replace(day=1)
        next_two_month = (next_month+timedelta(days=32)).replace(day=1)
        next_three_month = (next_two_month+timedelta(days=32)).astimezone(pytz.timezone('Asia/Jakarta')).replace(day=now.day, hour=start_time.hour, minute=start_time.minute)
        for i in range(1, 12):
            if main_agenda.start_time + timezone.timedelta(days=i*7) > next_three_month:
                break
            
            day_name = timezone.now().strftime('%A')
            if day_name.lower() in ['saturday', 'sunday']:
                continue
            
            next_start_time = main_agenda.start_time + timezone.timedelta(days=i*7)
            next_end_time = main_agenda.end_time + timezone.timedelta(days=i*7)
            
            TeacherAgenda.objects.create(
                user=request.user,
                subject=subject,
                start_time=next_start_time,
                end_time=next_end_time,
                reference=reference,
            )
            
    if id:
        try:
            agenda = TeacherAgenda.objects.get(id=id, user=request.user)
        except TeacherAgenda.DoesNotExist:
            return HttpResponse(status=404)
        
        start_time_delta = agenda.start_time-start_time
        end_time_delta = agenda.end_time-end_time
        
        agenda.subject=subject
        agenda.start_time=start_time
        agenda.end_time=end_time
        agenda.save()
        
        if apply_changes_to == 'this':
            if start_time_delta.seconds/60 >= 1 and end_time_delta.seconds/60 >= 1:
                agenda.reference = None
                agenda.save()
                
        if apply_changes_to == 'related':
            if not agenda.reference:
                return redirect('schedule')
            for agenda_ in TeacherAgenda.objects.filter(reference=agenda.reference, start_time__gt=start_time):
                agenda_.start_time = agenda_.start_time + timezone.timedelta(days=start_time_delta.days, seconds=start_time_delta.seconds)
                agenda_.end_time = agenda_.end_time + timezone.timedelta(days=end_time_delta.days, seconds=end_time_delta.seconds)
                agenda_.subject=subject
                agenda_.save()
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
    if today and agenda_list:
        nearest_today_agenda = min(agenda_list, key=lambda x: abs(x['date'] - today))
    
    context = {
        'agenda_list': agenda_list,
        'nearest_today_agenda': nearest_today_agenda,
        'today': today,
        'init_flowbite': init_flowbite,
        'total_questions': ReflectionQuestion.objects.count(),
    }
    return render(request, 'core/journal/schedule-items.html', context)


@login_required
def refleksi_input(request, id, refleksi=None):
    if not refleksi:
        refleksi = 1
    
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
            'page_title': "Refleksi",
        }
    else:
        schedule = request.POST.get('schedule',None)
        order = request.POST.get('order',None)
        refleksi_answer = request.POST.get('refleksi_answer',None)

        schedule = TeacherAgenda.objects.get(id=schedule)
        question = ReflectionQuestion.objects.get(order=order)
        subject = schedule.subject
        jurnal,_ = Journal.objects.get_or_create(agenda=schedule,question=question)
        
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

@login_required
def summary_refleksi(request, id):
    try:
        schedule = TeacherAgenda.objects.get(id=id)
    except TeacherAgenda.DoesNotExist:
        return HttpResponse(status=404)
    journals = Journal.objects.filter(agenda=schedule).order_by('created_at')
    summary = ''
    for journal in journals:
        # get the last character of jhournal.content
        if not journal.content:
            continue
        last_char = journal.content.strip()[-1]
        if last_char not in ['.', '?', '!', ]:
            summary += journal.content.strip().capitalize() + '. '
        else:
            summary += journal.content.strip().capitalize() + ' '
        print(summary.capitalize())
    context = {
        'summary': summary
    }
    return render(request, 'core/journal/refleksi-summary.html', context)
