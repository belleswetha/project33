from django.shortcuts import render


# Create your views here.
from django.core.mail import send_mail
from app.forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from app.models import *



def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid()and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            send_mail ('registration',
                       'thank u ur registration form is succesfully completed',
                       'belleswetha2002@gmail.com',
                       [MUFDO.email],
                       fail_silently=True
                       )
            return HttpResponse('Registration is sucessfully')
        
    return render(request,'registration.html',d)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')
  
def user_login(request):
    if request.method=="POST":
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home')) 


@login_required
def profile_display(request):
    un=request.session.get('username')
    Uo=User.objects.get(username=un)
    po=Profile.objects.get(username=Uo)
    d={'UO':Uo,'po':po}

    return render(request,'profile_display.html',d)


@login_required
def change_password(request):
    if request.method=="POST":
        pw=request.POST['pw']
        username=request.session.get('username')
        Uo=User.objects.get(username=username)
        Uo.set_password('pw')
        Uo.save()
        return HttpResponse('Password changed successfully')
    return render(request,'change_password.html') 

def reset_password(request):
    if request.method=="POST":
        username=request.POST['un']
        password=request.POST['pw']
        LUO=User.objects.filter(username=username)
        if LUO:
            Uo=LUO[0]
            Uo.set_password('password')
            Uo.save()
            return HttpResponse('reset password is done')

        else:
            return HttpResponse('ur username is not entered in our details')

    return render(request,'reset_password.html')


        
