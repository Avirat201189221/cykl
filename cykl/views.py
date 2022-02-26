from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import cykl
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.core.mail import send_mail
# Create your views here.

def index(request):
    return render(request,'index.html')


def register(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                subject='Thank you for registering to cykl'
                body = 'Thank you for registering to cykl. We sincerely hope you have fun riding cykls'
                send_mail(
                    subject,
                    body,
                    'chandravo26174.dpskalyanpur@gmail.com',
                    [email],
                    fail_silently = False,
                )
                return render(request,'login.html')
            
        else:
            messages.info(request,'passwords do not match')
            return redirect('register')
    else:
        return render(request,'register.html')


def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return render(request,'login.html')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('index.html')
    else:
        return render (request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def rent(request):
    return render(request, 'rent.html')