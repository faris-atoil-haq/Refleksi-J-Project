import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from config.settings import AWS_LOCATION, AWS_STORAGE_BUCKET_NAME, S3_CLIENT
from core.models import Module, ModuleAssessment, Subject
from utils.chatpdf import ChatPDF


@login_required
def module(request,subject=None):
    print(request.POST)
    page_title = 'Modul'
    user = request.user
    query = None

    if subject:
        page_title = 'Modul'
        subject = Subject.objects.get(id=subject)
        modules = Module.objects.filter(user=user,subject=subject)    

        context = {
            'page_title': page_title,
            'page': 'module',
            'modules': modules,
            'subject': subject,
        }
        
        if 'name' in request.POST:
            subject.name = request.POST.get('name')
            subject.save()
            return render(request, 'core/module/module-edit.html', {'subject':subject})

        else:
            return render(request, 'core/module/module-list.html', context)
    
    # Main Module
    if request.GET.get('search'):
        query = request.GET.get('search')
        subjects = Subject.objects.filter(user=user,name__icontains=query.lower())    
    else:
        subjects = Subject.objects.filter(user=user)
    context = {
        'page_title': page_title,
        'page': 'module',
        'subjects': subjects,
        'query': query if query else None,
    }
    return render(request, 'core/module/module-main.html', context)

@login_required
def subject_manager(request, subject_id=None):
    """Create or edit a subject"""
    user=request.user
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
            return render(request, 'core/module/module-subject-item.html', context=context)
        
        else:
            if not name:
                return HttpResponse(status=400)
            order_ = len(Subject.objects.filter(user=user)) + 1
            subject_ = Subject.objects.create(name=name,user=user,order=order_)
        return redirect('module')
    
    # GET METHOD
    context = {
        'page_title': 'Tambah Mata Pelajaran'
    }
    return render(request, 'core/module/module-create-subject.html', context)

def upload_module(request):
    print(request.POST)
    module_file = request.FILES.get('module_file',None)
    subject_id = request.POST.get("subject",None)
    try:
        if module_file and subject_id:
            subject = Subject.objects.get(id=subject_id)
            # remove extension
            module_file.name = module_file.name.replace('.'+module_file.name.split('.')[-1], '')
            # Add timestamp to avoid duplicated file name
            module_file.name = f"{module_file.name}_{int(timezone.now().timestamp())}"
            module_obj = Module.objects.create(user=request.user,subject=subject)
            module_obj.name = module_file.name
            module_obj.module_file = module_file
            module_obj.save()
    except Exception as e:
        print("Error Upload Modul: ",e)

    return redirect(reverse('module_subject',kwargs={'subject': subject_id}))

@login_required
@require_POST
def delete_module(request, id):
    module_obj = Module.objects.filter(id=id, user=request.user)
    if module_obj:
        module_obj = module_obj[0]
        module_obj.delete()

    return redirect('module')

@login_required
@require_GET
def upload_to_chatpdf(request, id):
    try:
        module = Module.objects.get(id=id, user=request.user)
    except Module.DoesNotExist:
        return HttpResponse(status=404)
    
    response = HttpResponse()
    response['HX-Trigger'] = json.dumps({'generateFeedback'+str(id).replace('-', ''):''})
    if not module.chatpdf_id:
        chatpdf = ChatPDF()
        res = chatpdf.upload_pdf(module.module_file.url)
        if res:
            module.chatpdf_id = res
            module.save()
    return response
    
@login_required
@require_GET
def check_module_components(request,id):
    try:
        module = Module.objects.get(id=id, user=request.user)
    except Module.DoesNotExist:
        return HttpResponse(status=404)
    
    chatpdf = ChatPDF()
    if module.chatpdf_id:
        res = chatpdf.check_must_have_components(module.chatpdf_id)
        if type(res) == dict:
            ModuleAssessment.objects.create(category='komponen_wajib', module=module, response_json=res)
        elif type(res) == str:
            ModuleAssessment.objects.create(category='komponen_wajib', module=module, response=res)
    else:
        return HttpResponse(status=404)
    response = HttpResponse()
    response['HX-Trigger'] = json.dumps({'checkComponentsDone':''})
    return response
    
@login_required
@require_GET
def generate_module_assessment(request, id):
    try:
        module = Module.objects.get(id=id, user=request.user)
    except Module.DoesNotExist:
        return HttpResponse(status=404)
    
    chatpdf = ChatPDF()
    if module.chatpdf_id:
        res = chatpdf.provide_assessment(module.chatpdf_id)
        if type(res) == dict:
            ModuleAssessment.objects.create(category='penialaian_kesesuaian', module=module, response_json=res)
        elif type(res) == str:
            ModuleAssessment.objects.create(category='penialaian_kesesuaian', module=module, response=res)
    else:
        print('Module is not uploaded to the ChatPDF yet.')
        return HttpResponse(status=404)
    
    response = HttpResponse()
    response['HX-Trigger'] = json.dumps({'suitabilityAssessmentDone':''})
    return response

@login_required
@require_GET
def generate_suggestion(request, id):
    try:
        module = Module.objects.get(id=id, user=request.user)
    except Module.DoesNotExist:
        return HttpResponse(status=404)
    
    chatpdf = ChatPDF()
    if module.chatpdf_id:
        res = chatpdf.get_suggestion(module.chatpdf_id)
        ModuleAssessment.objects.create(category='suggestion', module=module, response=res)
    else:
        print('Module is not uploaded to the ChatPDF yet.')
        return HttpResponse(status=404)
    
    response = HttpResponse()
    response['HX-Trigger'] = json.dumps({'suggestionDone':''})
    return response

@login_required
@require_GET
def get_feedback(request, id):
    try:
        module = Module.objects.get(id=id, user=request.user, chatpdf_id__isnull=False)
    except Module.DoesNotExist:
        return HttpResponse(status=404)
    
    feedbacks = []
    try:
        module_assessment = ModuleAssessment.objects.get(module=module, category='komponen_wajib', response_json__isnull=False)
    except ModuleAssessment.DoesNotExist:
        chatpdf = ChatPDF()
        res = chatpdf.check_must_have_components(module.chatpdf_id)
        if type(res) == dict:
            module_assessment = ModuleAssessment.objects.create(category='komponen_wajib', module=module, response_json=res)
        elif type(res) == str:
            ModuleAssessment.objects.create(category='komponen_wajib', module=module, response=res)
            module_assessment = None
        else:
            return HttpResponse(status=404)
    if module_assessment:
        feedbacks.append(module_assessment)
    
    try:
        module_assessment = ModuleAssessment.objects.get(module=module, category='penialaian_kesesuaian', response_json__isnull=False)
    except ModuleAssessment.DoesNotExist:
        chatpdf = ChatPDF()
        res = chatpdf.provide_assessment(module.chatpdf_id)
        if type(res) == dict:
            module_assessment = ModuleAssessment.objects.create(category='penialaian_kesesuaian', module=module, response_json=res)
        elif type(res) == str:
            ModuleAssessment.objects.create(category='penialaian_kesesuaian', module=module, response=res)
            module_assessment = None
        else:
            return HttpResponse(status=404)
    if module_assessment:
        feedbacks.append(module_assessment)
        
    try:
        module_assessment = ModuleAssessment.objects.get(module=module, category='suggestion', response__isnull=False)
    except ModuleAssessment.DoesNotExist:
        chatpdf = ChatPDF()
        res = chatpdf.get_suggestion(module.chatpdf_id)
        module_assessment = ModuleAssessment.objects.create(category='suggestion', module=module, response=res)
    feedbacks.append(module_assessment)
    
    return render(request, 'core/module/module-feedback.html', {'feedbacks': feedbacks})

@login_required
@require_GET
def get_view_feedback_btn(request, id):
    return render(request, 'core/module/view-feedback-btn.html', {'module':{'id': id}})

@login_required
@require_POST
def module_name(request, id):
    try:
        modul = Module.objects.get(id=id, user=request.user)
    except Module.DoesNotExist:
        return HttpResponse(status=404)
    
    modul.name = request.POST.get('name')
    modul.save()
    return redirect('module_subject', subject=modul.subject.id)