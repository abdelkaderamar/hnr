from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

from .forms import UserCreateForm
# Create your views here.

def loginaccount(request):   
    print(f"#### {request.method}") 
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
             {'form':AuthenticationForm})            
    else:
        user = authenticate(request, username=request.POST['username'],
        password=request.POST['password'])            
        if user is None:                                
            return render(request,'accounts/login.html',
                        {'form': AuthenticationForm(),
                            'error': 'username and password do not match'})
        else:
            login(request,user)
            return redirect('home')

def logoutaccount(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'GET':
        context = {'form': UserCreateForm}
        return render(request, 'accounts/signup.html', context)
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(request.POST['username'],
                        password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/signup.html',
                    {'form':UserCreateForm, 'error':'Passwords do not match'})
        except IntegrityError:
            return render(request, 'accounts/signup.html',
                 {'form':UserCreateForm,
                 'error':'Username already taken. Choose new username.'})