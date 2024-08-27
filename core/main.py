import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from core.models import (AngketAnswerOption, AngketQuestion,
                         ReflectionQuestion, Subject, Verification)
from utils.mail import send_email


@login_required
def home(request):
    page_title = 'Home'
    context = {
        'page_title': page_title,
        'page': 'home',
    }
    return render(request, 'core/home.html', context)

@login_required
def app_settings(request):
    page_title = 'Admin'
    context = {
        'page_title': page_title,
        'page': 'admin',
    }
    return render(request, 'core/settings/settings.html', context)

@login_required
def reflection_templates(request):
    reflection_questions = ReflectionQuestion.objects.all().order_by('order')
    context = {
        'page_title': 'Admin',
        'page': 'admin',
        'reflection_questions': reflection_questions,
    }
    return render(request, 'core/settings/reflection/manage-reflection-template.html', context)

@login_required
def manage_reflection_question(request, id=None):
    if id:
        try:
            reflection_question = ReflectionQuestion.objects.get(id=id)
        except:
            return HttpResponse(status=404)
        if request.POST.get('delete'):
            current_order = reflection_question.order
            ReflectionQuestion.objects.filter(order__gt=current_order).update(order=F('order') - 1)
            reflection_question.delete()
            return redirect('reflection_templates')
    else:
        questions = ReflectionQuestion.objects.all()
        reflection_question = ReflectionQuestion.objects.create(order=len(questions) + 1)
    
    reflection_question.question = request.POST.get('question', reflection_question.question)
    reflection_question.save()
    context = {
        'id': reflection_question.id,
        'order': reflection_question.order,
        'question': reflection_question.question
    }
    return render(request, 'core/settings/reflection/reflection-question-card.html', context)

@login_required
def order_reflection_question(request):
    ids = request.POST.getlist('id')
    if not ids:
        return HttpResponse(status=400)
    
    for order, question_id in enumerate(ids, start=1):
        try:
            reflection_question = ReflectionQuestion.objects.get(id=question_id)
            reflection_question.order = order
            reflection_question.save()
        except ReflectionQuestion.DoesNotExist:
            return HttpResponse(status=404)
    return render(request, 'core/settings/reflection/reflection-questions.html', {'reflection_questions': ReflectionQuestion.objects.all().order_by('order')})

@login_required
def angket_templates(request):
    angket_questions = AngketQuestion.objects.all().order_by('order')
    context = {
        'page_title': 'Admin',
        'page': 'admin',
        'angket_questions': angket_questions,
    }
    return render(request, 'core/settings/angket/manage-angket-template.html', context)

@login_required
def manage_angket_question(request, id=None):
    if id:
        try:
            angket_question = AngketQuestion.objects.get(id=id)
        except:
            return HttpResponse(status=404)
        if request.POST.get('delete'):
            current_order = angket_question.order
            AngketQuestion.objects.filter(order__gt=current_order).update(order=F('order') - 1)
            angket_question.delete()
            return redirect('angket_templates')
    else:
        questions = AngketQuestion.objects.all()
        angket_question = AngketQuestion.objects.create(order=len(questions) + 1)
    
    angket_question.question = request.POST.get('question', angket_question.question)
    angket_question.description = request.POST.get('description', angket_question.description)
    angket_question.save()
    context = {
        'id': angket_question.id,
        'order': angket_question.order,
        'question': angket_question.question,
        'description': angket_question.description
    }
    return render(request, 'core/settings/angket/angket-question-card.html', context)

@login_required
def order_angket_question(request):
    ids = request.POST.getlist('id')
    if not ids:
        return HttpResponse(status=400)
    
    for order, question_id in enumerate(ids, start=1):
        try:
            angket_question = AngketQuestion.objects.get(id=question_id)
            angket_question.order = order
            angket_question.save()
        except AngketQuestion.DoesNotExist:
            return HttpResponse(status=404)
    return render(request, 'core/settings/angket/angket-questions.html', {'angket_questions': AngketQuestion.objects.all().order_by('order')})

@login_required
def manage_angket_option(request, angket_id, id=None):
    try:
        angket_question = AngketQuestion.objects.get(id=angket_id)
    except:
        return HttpResponse(status=404)
    
    print(request.GET)
    if id:
        try:
            answer_option = AngketAnswerOption.objects.get(id=id, question=angket_question)
        except:
            return HttpResponse(status=404)
        
        if request.GET.get('delete'):
            current_order = answer_option.order
            AngketAnswerOption.objects.filter(question=angket_question, order__gt=current_order).update(order=F('order') - 1)
            answer_option.delete()
            return HttpResponse(status=200)
    else:
        answer_option = AngketAnswerOption.objects.create(question=angket_question, order=len(AngketAnswerOption.objects.all()) + 1)
    
    answer_option.text = request.GET.get('text', answer_option.text)
    answer_option.save()
    context = {
        'question_id': angket_id,
        'option_id': answer_option.id,
        'text': answer_option.text,
        'order': answer_option.order,
    }
    return render(request, 'core/settings/angket/option-card.html', context)

@login_required
def order_angket_option(request, angket_id):
    print(request.POST)
    ids = request.POST.getlist('option_id')
    if not ids:
        return HttpResponse(status=400)
    
    for order, id_ in enumerate(ids, start=1):
        try:
            answer_option = AngketAnswerOption.objects.get(question__id=angket_id, id=id_)
            answer_option.order = order
            answer_option.save()
        except AngketAnswerOption.DoesNotExist:
            return HttpResponse(status=404)
    return render(request, 'core/settings/angket/angket-questions.html', {'answer_options': AngketAnswerOption.objects.filter(question__id=angket_id).order_by('order')})


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            try:
                verif = Verification.objects.get(user=user)
            except Verification.DoesNotExist:
                verif = None
            if verif and verif.verified == True:
                login(request, user)
                return redirect('home')
        
        error_message = "Email atau kata sandi salah."
        context = {
            "email": email,
            "error_message": error_message,
        }
        return render(request, 'core/login.html', context=context)
    return render(request, 'core/login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        email = request.POST.get('email')
        nama = request.POST.get('nama')
        instansi = request.POST.get('instansi')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        verif_code = str(uuid.uuid4())[:5]
        print("Kode verifikasi: ")
        print(verif_code)
        
        if confirm_password != password:
            return render(request, 'core/signup.html', {'error_message': 'Kata sandi tidak cocok.'})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                username=str(uuid.uuid4()),
                first_name=nama,
                password=password
            )
        verification = Verification.objects.filter(user=user).first()
        if not verification:
            verification, _ = Verification.objects.get_or_create(user=user)
            verification.verified = False
            verification.instansi = instansi
            verification.code = verif_code
            verification.save()
            
            confirm_signup_link = settings.PARENT_HOST + reverse('confirm')
            send_email('Verifikasi Akun',email,f'Selamat datang!\n\nKlik link verifikasi berikut untuk menggunakan akun Anda: \n{confirm_signup_link}/?code={verif_code}&email={email}')
        

        return render(request, 'core/confirm.html')
    email = request.GET.get('email', None)
    return render(request, 'core/signup.html', {'email': email})

def confirm(request):
    verif_code = request.GET.get('code')
    email = request.GET.get('email')

    user = User.objects.filter(email=email).first()
    if user:
        verif = Verification.objects.filter(user=user).first()
        if verif_code == verif.code:
            verif.verified = True
            verif.save()
            return render(request, 'core/confirm.html',{'verified':True,'option':'signup'})

    return render(request, 'core/confirm.html')

def reset_password_email(request):
    if request.POST:
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            verif = Verification.objects.filter(user=user).first()
            if verif.verified:
                code = str(uuid.uuid4())
                verif.code = code
                verif.save()
                reset_password_link = settings.PARENT_HOST+reverse('reset_password')+f'?email={email}&code={code}'
                print("Reset Password Link: ",reset_password_link)
                send_email('Reset Password', email, f'Klik link berikut untuk mereset kata sandi Anda: \n{reset_password_link}')
            else:
                link_verifikasi = settings.PARENT_HOST+reverse('confirm')+f'?email={email}&code={verif.code}'
                print("Email belum terverifikasi. Link: ",link_verifikasi)
                send_email('Reset Password',email,f'Halo,\nAnda ingin melakukan pengaturan kata sandi Anda, namun kami melihat bahwa Anda belum menyelesaikan verifikasi email. Klik tautan berikut untuk melakukan verifikasi: \n{link_verifikasi}')
        else:
            signup_link = settings.PARENT_HOST+reverse('signup')+f'?email={email}'
            print("Email belum terdaftar. Link: ",signup_link)
            send_email('Reset Password',email,f'Halo,\nAnda ingin melakukan pengaturan kata sandi Anda, namun kami tidak menemukan email Anda. Daftarkan email Anda di sini: \n{signup_link}')
        return redirect(reverse('confirm')+'?email='+email)
    return render(request, 'core/reset_password_email.html')


def reset_password(request):
    if request.GET:
        email = request.GET.get('email')
        code = request.GET.get('code')

        user = User.objects.filter(email=email).first()
        if user:
            verif = Verification.objects.filter(user=user).first()
            if verif.verified and code == verif.code:
                return render(request, 'core/reset_password.html',{'verified':True, 'email':email})
    if request.POST:
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user:
            user = user[0]
            if 'confirm_password' in request.POST:
                password = request.POST.get('password')
                user.set_password(password)
                user.save()

                return render(request, 'core/confirm.html',{'verified':True,'option':'reseted'})
            else:
                verif_code = str(uuid.uuid4())
                print("Reset Code: ",verif_code)
                verif = user.verification
                verif.code = verif_code
                verif.save()
                
                return render(request, 'core/confirm.html',{'verified':True,'option':'reset'})
            
    return redirect('reset_password_email')

def signout(request):
    if not request.user.is_authenticated:
        return redirect('public')
    
    logout(request)
    return redirect('public')
