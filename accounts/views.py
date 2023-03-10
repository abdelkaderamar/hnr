from ast import keyword
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

from rich import inspect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

from .forms import SignupForm
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

def send_mail(user):
    app_secret = config("MAIL_SECRET")
    username = config("MAIL_USER")
    smtp_server = config("SMTP_HOST")
    smtp_port = config("SMTP_PORT")
    recipient = config("RECIPIENT")
    print(f'{username} | {app_secret} | {smtp_server}:{smtp_port} | {recipient}')

    # create a message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = recipient
    msg['Subject'] = '[HNR] A new user signup'
    body = f'A new user has registered. Username = {user.username}'
    msg.attach(MIMEText(body, 'plain'))

    # send the message
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, app_secret)
        server.sendmail(username, recipient, msg.as_string())

def signup(request):
    if request.method == 'GET':
        context = {'form': SignupForm}
        return render(request, 'accounts/signup.html', context)
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(request.POST['username'],
                        password=request.POST['password1'], is_active=False)
                user.save()
                # login(request, user)
                send_mail(user)
                return render(request, 'accounts/signup.html',
                    {'form': SignupForm, 'success':'User created but needs to be validated by an admin before being able to connect'})
            else:
                return render(request, 'accounts/signup.html',
                    {'form': SignupForm, 'error':'Passwords do not match'})
        except IntegrityError:
            return render(request, 'accounts/signup.html',
                 {'form': SignupForm,
                 'error':'Username already taken. Choose new username.'})


@login_required
def user_profile(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user_id=user.id).first()
    if user_profile is None:
        user_profile = UserProfile(user=user, keywords="")
        user_profile.save()
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
    story_per_page = int(request.POST['story_per_page'])
    hightlight_score_threshold = int(request.POST['hightlight_score_threshold'])
    hightlight_comment_threshold = int(request.POST['hightlight_comment_threshold'])
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
    user = request.user
    user_profile = UserProfile.objects.filter(user_id=user.id).first()
    user_profile.keywords = keywords
    user_profile.story_per_page = story_per_page
    user_profile.hightlight_score_threshold = hightlight_score_threshold
    user_profile.hightlight_comment_threshold = hightlight_comment_threshold
    user_profile.save_and_hide = save_and_hide
    user_profile.default_display = default_display
    user_profile.open_hn_by_default = open_hn_by_default
    user_profile.open_in_new_tab = open_in_new_tab
    user_profile.startup_page = startup_page
    user_profile.save()
    return redirect("accounts:user_profile")

