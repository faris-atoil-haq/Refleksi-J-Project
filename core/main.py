import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from config.settings import AWS_LOCATION, AWS_STORAGE_BUCKET_NAME, S3_CLIENT
from core.models import Module, Subject, Verification


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
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except:
        page = 1
    q = request.GET.get('q', '')
    
    conditions = Q()
    if q:
        conditions = Q(subject__name__icontains=q)
        conditions |= Q(subject__class_levl__icontains=q)
    paginator = Paginator(
        SubjectReflection.objects.filter(conditions).distinct().order_by('-created_at'), 
        25
    )
    if page > paginator.num_pages:
        page = 1
    current_page = paginator.page(page)
    objects = current_page.object_list
        
    context = {
        'page_title': 'Template Refleksi',
        'page': page,
        'current_page': current_page,
        'paginator': paginator,
        'q': q,
        'subject_reflections': objects,
    }
    return render(request, 'core/settings/reflection/reflection.html', context)

@login_required
def manage_reflection_template(request, id=None):
    context = {
        'page_title': 'Template Refleksi'
    }
    return render(request, 'core/settings/reflection/reflection.html', context)

@login_required
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
    return render(request, 'core/settings/subject/subjects.html', context)

@login_required
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
            return render(request, 'core/settings/subject/subject-item.html', context=context)
        
        else:
            if not name:
                return HttpResponse(status=400)
            
            subject_ = Subject.objects.create(name=name)
        return redirect('subject_page')
    
    # GET METHOD
    context = {
        'page_title': 'Tambah Mata Pelajaran'
    }
    return render(request, 'core/settings/subject/create-subject.html', context)

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
            
            # send_email('Verifikasi Akun',email,f'Selamat datang!\n\nKlik link verifikasi berikut untuk menggunakan akun Anda: \n{confirm_signup_link}/?code={verif_code}&email={email}')
        

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
                reset_password_link = request.build_absolute_uri(reverse('reset_password')+f'?email={email}&code={code}')
                print("Reset Password Link: ",reset_password_link)
                # send_email('Reset Password', email, f'Klik link berikut untuk mereset kata sandi Anda: \n{reset_password_link}/?code={code}&email={email}')
                # send_email('Reset Password',email,f'Klik link berikut untuk mereset kata sandi Anda: \n{reset_password_link}/?code={code}&email={email}')
            else:
                reset_password_link = request.build_absolute_uri(reverse('confirm')+f'?email={email}&code={verif.code}')
                print("Email belum terverifikasi. Link: ",reset_password_link)
                # send_email('Reset Password',email,f'Halo,\nAnda ingin melakukan pengaturan kata sandi Anda, namun kami melihat bahwa Anda belum menyelesaikan verifikasi email. Klik tautan berikut untuk melakukan verifikasi: \n{link_verifikasi}')
        else:
            reset_password_link = request.build_absolute_uri(reverse('signup')+f'?email={email}')
            print("Email belum terdaftar. Link: ",reset_password_link)
            # send_email('Reset Password',email,f'Halo,\nAnda ingin melakukan pengaturan kata sandi Anda, namun kami tidak menemukan email Anda. Daftarkan email Anda di sini: \n{signup_link}')
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
