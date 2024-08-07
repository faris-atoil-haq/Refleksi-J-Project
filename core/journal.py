from django.shortcuts import render
from django.utils import timedelta, timezone

from core.models import *


def today_agenda(request):
    agenda_list = TeacherAgenda.objects.filter(
        start_time=timezone.now().replace(hour=0, minute=0, second=0) + timedelta(hours=7)
    ).order_by('start_time')

    context = {
        'agenda_list': agenda_list,
    }
    return render(request, 'core/journal/today-agenda.html', context)

def agenda(request):
    TeacherAgenda.objects.filter().order_by('start_time')