from ast import keyword
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

from rich import inspect

from .forms import UserCreateForm
from .models import UserProfile

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

@login_required
def user_profile(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user_id=user.id).first()
    if user_profile is None:
        user_profile = UserProfile(user=user, keywords="")
        user_profile.save()
    print(user_profile.max_story)
    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/user_profile.html', context)

@login_required
def save_profile(request):
    print("Saving the profile")
    username = request.POST['username']
    keywords = request.POST['keywords']
    max_story = int(request.POST['max_story'])
    save_and_hide = bool(request.POST.get('save_and_hide'))
    print(f"save_and_hide={save_and_hide}")
    open_hn_by_default = bool(request.POST.get('open_hn_by_default'))
    print(f"open_hn_by_default={open_hn_by_default}")
    default_display_str=(request.POST.get("default_display"))
    print(f"default_display_str={default_display_str}")
    if default_display_str == 'recent_stories':
        default_display = -1
    elif default_display_str == 'old_stories':
        default_display = -2
    else:
        default_display = 0
    open_in_new_tab = bool(request.POST.get('open_in_new_tab'))
    print(f"open_in_new_tab={open_in_new_tab}")

    startup_page=request.POST.get('startup_page')

    inspect(username)
    inspect(keywords)
    inspect(max_story)
    user = request.user
    user_profile = UserProfile.objects.filter(user_id=user.id).first()
    user_profile.keywords = keywords
    user_profile.max_story = max_story
    user_profile.save_and_hide = save_and_hide
    user_profile.default_display = default_display
    user_profile.open_hn_by_default = open_hn_by_default
    user_profile.open_in_new_tab = open_in_new_tab
    user_profile.startup_page = startup_page
    user_profile.save()
    return redirect("accounts:user_profile")

