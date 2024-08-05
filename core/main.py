from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from core.models import Subject


def home(request):
    page_title = 'Home'
    context = {
        'page_title': page_title,
    }
    return render(request, 'core/home.html', context)

def app_settings(request):
    page_title = 'Application Settings'
    context = {
        'page_title': page_title,
    }
    return render(request, 'core/settings/settings.html', context)

def subject_page(request):
    page_title = 'Mata Pelajaran'
    
    try:
        page = int(request.GET.get('page', 1))
    except:
        return HttpResponse(status=400)
    if page < 1:
        page = 1
    q = request.GET.get('q', '')
    
    conditions = Q()
    if q:
        conditions = Q(name__icontains=q)
    paginator = Paginator(
        Subject.objects.filter(conditions).order_by('name'), 
        25
    )
    if page > paginator.num_pages:
        page = 1
    current_page = paginator.page(page)
    subjects = current_page.object_list
        
    context = {
        'page_title': page_title,
        'page': page,
        'current_page': current_page,
        'paginator': paginator,
        'q': q,
        'subjects': subjects,
    }
    return render(request, 'core/settings/subjects.html', context)

def subject(request, subject_id=None):
    """Create or edit a subject"""
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if subject_id:
            is_delete = request.POST.get('delete')
            if not (name or is_delete):
                return HttpResponse(status=400)
            
            try:
                subject_ = Subject.objects.get(id=subject_id)
                if is_delete:
                    subject_.delete()
                    return HttpResponse()
                else:
                    subject_.name = name
                    subject_.save()
            except:
                return HttpResponse(status=404)
            context = {
                'subject': subject_
            }
            return render(request, 'core/settings/subject-item.html', context=context)
        
        else:
            if not name:
                return HttpResponse(status=400)
            
            subject_ = Subject.objects.create(name=name)
        return redirect('subject_page')
    
    # GET METHOD
    context = {
        'page_title': 'Tambah Mata Pelajaran'
    }
    return render(request, 'core/settings/create-subject.html', context)