import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.models import AngketQuestion, AngketResponse, AngketSession


@login_required
@require_GET
def main(request):
    user = request.user  # Assuming you have user authentication implemented
    angket_sessions = AngketSession.objects.filter(user=user).order_by('-created_at')
    
    paginator = Paginator(angket_sessions, 20)  # Create a Paginator object with 20 items per page
    page_number = request.GET.get('page')  # Get the current page number from the request's GET parameters
    page_obj = paginator.get_page(page_number)  # Get the Page object for the current page
    
    # Get previous page number
    previous_page_number = page_obj.previous_page_number() if page_obj.has_previous() else None
    
    # Get next page number
    next_page_number = page_obj.next_page_number() if page_obj.has_next() else None
    
    context = {
        'page': 'angket',
        'page_title': 'Angket',
        'angkets': page_obj,
        'previous_page_number': previous_page_number,
        'next_page_number': next_page_number,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    }
    
    return render(request, 'core/angket/main.html', context)

@login_required
@require_POST
def generate_angket(request):
    angket_session = AngketSession.objects.create(user=request.user)
    angket_session.name = str(angket_session.id)
    angket_session.link = settings.PARENT_HOST + '/angket/' + str(angket_session.id) + '/'
    angket_session.save()
    
    return redirect('angket')

@login_required
def delete_angket(request, id):
    try:
        angket_session = AngketSession.objects.get(id=id, user=request.user)
    except AngketSession.DoesNotExist:
        return HttpResponse(status=404)
    angket_session.delete()
    
    return redirect('angket')

@login_required
def angket_form(request, id):
    try:
        angket_session = AngketSession.objects.get(id=id, user=request.user)
    except AngketSession.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        context = {
            'angket': angket_session
        }
        return render(request, 'core/angket/angket-form.html', context)

    name = request.POST.get('name')
    if not name:
        return HttpResponse(status=400)
    angket_session.name=name
    angket_session.save()
    return HttpResponse()

@login_required
@require_POST
def toggle_accept_response(request, id):
    try:
        angket_session = AngketSession.objects.get(id=id, user=request.user)
    except AngketSession.DoesNotExist:
        return HttpResponse(status=404)
    accept_response = request.POST.get('accept_response')
    angket_session.accept_response = True if accept_response == 'on' else False
    angket_session.save()
    
    return HttpResponse()

@login_required
@require_GET
def public_angket(request, id):
    try:
        angket_session = AngketSession.objects.get(id=id)
    except AngketSession.DoesNotExist:
        return HttpResponse(status=404)
    
    if not angket_session.accept_response:
        return HttpResponse('Anda tidak dapat mengakses halaman ini.', status=403)
    
    page = None
    session_id = request.session.get('session_id')
    if not session_id:
        request.session['session_id'] = str(uuid.uuid4())
    else:
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            print(e)
            page = None
    
    if page:
        try:
            question_number = page
            angket_question = AngketQuestion.objects.get(order=page)
            print(f'{angket_question.order=}')
        except:
            return HttpResponse(status=404)
    else:
        question_number = 1
        angket_question = AngketQuestion.objects.all().order_by('order').first()
    
    try:
        ar = AngketResponse.objects.get(
            session=angket_session,
            respondent=session_id, 
            question=angket_question, 
            question_text=angket_question.question,
        )
        print(ar.__dict__)
    except AngketResponse.DoesNotExist:
        ar = None
    total_questions = AngketQuestion.objects.count()
    
    context = {
        'no_sidebar': True,
        'page_title': 'Angket',
        'page': 'angket',
        'question_number': question_number,
        'angket_session': angket_session,
        'angket_question': angket_question,
        'total_questions': total_questions,
        'user_response': ar,
    }
    return render(request, 'core/angket/public.html', context)

@login_required
@require_POST
def respond_angket(request, id):
    try:
        angket_session = AngketSession.objects.get(id=id)
    except AngketSession.DoesNotExist:
        print('AngketSession does not exist')
        return HttpResponse(status=404)
    
    session_id = request.session.get('session_id')
    if not session_id:
        print('User session does not exist')
        return redirect('public_angket', id=angket_session.id)
    
    question_id = request.POST.get('question_id')
    print(request.POST)
    try:
        angket_question = AngketQuestion.objects.get(id=question_id)
    except AngketQuestion.DoesNotExist:
        print('AngketQuestion does not exist')
        return HttpResponse(status=404)
    answer = request.POST.get('answer')
    
    ar, _ = AngketResponse.objects.get_or_create(
        session=angket_session,
        respondent=session_id, 
        question=angket_question, 
        question_text=angket_question.question,
    )
    ar.answer = answer
    ar.answer_options = {
        "option_range": angket_question.option_range,
        "option_step": angket_question.option_step,
        "option_start_label": angket_question.option_start_label,
        "option_end_label": angket_question.option_end_label,
        }
    ar.save()
    if angket_question == AngketQuestion.objects.all().order_by('order').last():
        return redirect('done_angket')
    return redirect(reverse('public_angket', args=[angket_session.id]) + f'?page={angket_question.order+1}')

@login_required
@require_GET
def angket_result(request, id):
    try:
        angket_session = AngketSession.objects.get(id=id, user=request.user)
    except AngketSession.DoesNotExist:
        return HttpResponse(status=404)

    question_distribution = {}
    responses = AngketResponse.objects.filter(session=angket_session).order_by('question__order')
    question_distribution_list = []
    for response in responses:
        question = response.question_text
        answer = response.answer
        if question not in question_distribution:
            question_distribution[question] = {}
        if answer not in question_distribution[question]:
            question_distribution[question][answer] = {'count': 0}
        question_distribution[question][answer]['count'] += 1
    
    for question, answers in question_distribution.items():
        total_responses = sum(answer['count'] for answer in answers.values())
        for answer in answers.values():
            answer['percentage'] = (answer['count'] / total_responses) * 100
        question_distribution_list.append({'question': question, 'answers': answers})
    context = {
        'angket_session': angket_session,
        'question_distribution': question_distribution_list
    }
    print(context)
    return render(request, 'core/angket/result.html', context)

@login_required
def done_angket(request):
    context = {
        'page': 'angket',
        'page_title': 'Angket',
        'no_sidebar': True,
    }
    return render(request, 'core/angket/done.html', context)