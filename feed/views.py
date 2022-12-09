from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from collections import OrderedDict
from datetime import datetime, timedelta
import os
import json

from rich import inspect

from accounts.models import UserProfile

from .task import create_random_user_accounts
from .models import Story, UserStory

from dataclasses import dataclass

@dataclass
class user_story_data:
    story: Story
    saved: bool = False
    ignored: bool = False

    def __str__(self):
        return self.story.__str__()

    def __repr__(self):
        return self.__str__()


def get_stories_page(request, stories):
    paginator = Paginator(stories, 25)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def fill_user_data(stories, user, include_ignored=False):
    if not user.is_authenticated:
        return [s for s in stories.values()]
    user_stories = UserStory.objects.filter(user_id=user.id)
    # print(len(user_stories))
    # print(stories)
    for us in user_stories:
        # print(f"checking {us.story_id}")
        if us.story_id in stories:
            # print(us.saved)
            stories[us.story_id].saved = us.saved
            stories[us.story_id].ignored = us.ignored
    if not include_ignored:
        return [s for s in stories.values() if s.ignored == False]
    return [s for s in stories.values()]

def get_user_keywords(user):
    user_keywords = []
    if user.is_authenticated:
        user_profile = UserProfile.objects.filter(user_id = user.id).first()
        if user_profile is not None:
            user_keywords = user_profile.keywords.split(';')
    return user_keywords

def sort_stories(request, all_stories, sort_param):
    if sort_param in ['time', 'score', 'descendants']:
        all_stories = all_stories.order_by(f'-{sort_param}')
    elif sort_param == 'ratio':
        all_stories = list(all_stories)
        all_stories.sort(key=lambda s : 0 if s.descendants == 0 else s.score/s.descendants, reverse=True)
    return all_stories

def get_context(request, all_stories):

    sort_param = request.GET.get("order_by")
    all_stories = sort_stories(request, all_stories, sort_param)
    stories = OrderedDict((s.id, user_story_data(s)) for s in all_stories)
    stories = fill_user_data(stories, request.user)
    stories_page = get_stories_page(request, stories)
    user_keywords = get_user_keywords(request.user)
    open_hn = False
    open_in_new_tab = False
    if request.user.is_authenticated:
        user_profile=UserProfile.objects.filter(user_id=request.user.id).first()
        if user_profile:
            open_hn=user_profile.open_hn_by_default
            open_in_new_tab=user_profile.open_in_new_tab

    context = {
        'stories': stories_page, 
        'user_keywords': user_keywords,
        'order_by': sort_param,
        'open_hn': open_hn,
        'open_in_new_tab': open_in_new_tab,
    }
    return context

def get_context_for_section(request, all_stories):
    if request.user.is_authenticated:
        user_profile=UserProfile.objects.filter(user_id=request.user.id).first()
        if user_profile:
            now = datetime.now()
            old_date = now - timedelta(days=1)
            if user_profile.default_display == UserProfile.OLD_STORIES:
                all_stories = all_stories.filter(time__lt=old_date)
            elif user_profile.default_display == UserProfile.RECENT_STORIES:
                all_stories = all_stories.filter(time__gte=old_date)
    return get_context(request, all_stories)

def home(request):
    return redirect('feed:index')

def index(request):
    all_stories = Story.objects.all().order_by('-time')
    context = get_context(request, all_stories)
    return render(request, 'feed/index.html', context)

def feed_admin(request):
    context = {}
    return render(request, 'feed/admin.html', context)

def refresh(request):
    pass

@login_required
def save(request, story_id):
    print(f"Saving the story {story_id}")
    saved_story = UserStory.objects.filter(Q(story_id=story_id) & Q(user_id=request.user.id)).first()
    user_profile = UserProfile.objects.filter(user_id=request.user.id).first()
    if user_profile:
        hide_story=user_profile.save_and_hide
    else:
        hide_story=False
    if saved_story is None:
        saved_story = UserStory()
        saved_story.story_id=int(story_id)
        saved_story.user_id=request.user.id
        saved_story.saved=True
        saved_story.ignored=hide_story
    else:
        saved_story.saved = True
        saved_story.ignored=hide_story
    saved_story.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, story_id):
    print(f"Deleting the story {story_id}")
    user_story = get_object_or_404(UserStory, story_id=story_id)
    user_story.saved = False
    user_story.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def save_single_story(user_id, story_id):
    saved_story = UserStory.objects.filter(Q(story_id=story_id) & Q(user_id=user_id)).first()
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if user_profile:
        hide_story=user_profile.save_and_hide
    else:
        hide_story=False
    if saved_story is None:
        saved_story = UserStory()
        saved_story.story_id=int(story_id)
        saved_story.user_id=user_id
        saved_story.saved=True
        saved_story.ignored=hide_story
    else:
        saved_story.saved = True
        saved_story.ignored=hide_story
    saved_story.save()


def hide_single_story(user_id, story_id, hide):
    saved_story = UserStory.objects.filter(Q(story_id=story_id) & Q(user_id=user_id)).first()
    if saved_story is None:
        saved_story = UserStory()
        saved_story.story_id=int(story_id)
        saved_story.user_id=user_id
        saved_story.saved=False
        saved_story.ignored=hide
    else:
        if hide:
            saved_story.ignored = hide
        else:
            saved_story.ignored = not saved_story.ignored
    saved_story.save()

@login_required
def hide(request, story_id):
    print(f"Hiding the story {story_id}")
    # saved_story = UserStory.objects.filter(Q(story_id=story_id) & Q(user_id=request.user.id)).first()
    # if saved_story is None:
    #     saved_story = UserStory()
    #     saved_story.story_id=int(story_id)
    #     saved_story.user_id=request.user.id
    #     saved_story.saved=False
    #     saved_story.ignored=True
    # else:
    #     saved_story.ignored = not saved_story.ignored
    # saved_story.save()    
    hide_single_story(request.user.id, story_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def top_stories(request):
    # print(f"request.GET = {request.GET}")
    print("top_stories request")
    all_stories = Story.objects.filter(Q(is_top=True)).order_by('-time')
    context = get_context_for_section(request, all_stories)
    context['list_type'] = 'top_stories'
    return render(request, 'feed/top_stories.html', context)


def best_stories(request):
    all_stories = Story.objects.filter(Q(is_best=True)).order_by('-time')
    context = get_context_for_section(request, all_stories)
    context['list_type'] = 'best_stories'
    return render(request, 'feed/best_stories.html', context)


def new_stories(request):
    all_stories = Story.objects.filter(Q(is_new=True)).order_by('-time')
    context = get_context_for_section(request, all_stories)
    context['list_type'] = 'new_stories'
    return render(request, 'feed/new_stories.html', context)

def ask_stories(request):
    all_stories = Story.objects.filter(Q(is_ask=True)).order_by('-time')
    context = get_context_for_section(request, all_stories)
    context['list_type'] = 'ask_stories'
    return render(request, 'feed/ask_stories.html', context)

def show_stories(request):
    all_stories = Story.objects.filter(Q(is_show=True)).order_by('-time')
    context = get_context_for_section(request, all_stories)
    context['list_type'] = 'show_stories'
    return render(request, 'feed/show_stories.html', context)

def job_stories(request):
    all_stories = Story.objects.filter(Q(is_job=True)).order_by('-time')
    context = get_context_for_section(request, all_stories)
    context['list_type'] = 'job_stories'
    return render(request, 'feed/job_stories.html', context)

def get_saved_stories(request):
    all_stories = UserStory.objects.filter(Q(user_id=request.user.id) &
            Q(saved=1))
    stories = dict((s.story.id, user_story_data(s.story)) for s in all_stories)
    stories = fill_user_data(stories, request.user, include_ignored=True)
    return stories

@login_required
def saved(request):
    stories = get_saved_stories(request)
    stories_page = get_stories_page(request, stories)
    user_keywords = get_user_keywords(request.user)
    context = {
        'stories': stories_page, 
        'user_keywords': user_keywords,
        'list_type': 'saved_stories',
    }
    return render(request, 'feed/saved_stories.html', context)

@login_required
def hidden(request):
    all_stories = UserStory.objects.filter(Q(user_id=request.user.id) &
            Q(ignored=1))
    stories = dict((s.story.id, user_story_data(s.story)) for s in all_stories)
    stories = fill_user_data(stories, request.user, include_ignored=True)        
    stories_page = get_stories_page(request, stories)
    user_keywords = get_user_keywords(request.user)
    context = {
        'stories': stories_page, 
        'user_keywords': user_keywords
    }
    return render(request, 'feed/ignored_stories.html', context)

@login_required
def custom_stories(request, key: str):
    all_stories = Story.objects.all().order_by('-time')
    inspect(all_stories)
    key = key.lower()
    all_stories = [s for s in all_stories if key in s.title.lower()]
    context = get_context(request, all_stories)
    return render(request, 'feed/index.html', context)

@login_required
def export_stories(request):
    file_name = os.path.join(settings.MEDIA_ROOT,
                         "test.txt")
    user_stories = UserStory.objects.filter(Q(user_id=request.user.id) &
            Q(saved=1))
    with open(file_name, 'w') as f:
        for user_story in user_stories:
            f.write(f"{user_story.story.title}\n")
            f.write(f"{user_story.story.url}\n")
            f.write(f"https://news.ycombinator.com/item?id={user_story.story.id}\n")
            f.write(f"\n")
    return FileResponse(open(file_name, "rb"), as_attachment=True)

@login_required
def clear_saved(request):
    all_stories = UserStory.objects.filter(user_id=request.user.id)
    for s in all_stories:
        s.saved = False
        s.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def hide_all(request):
    print("Hide all request")
    body = json.loads(request.body)
    ids = body['ids']
    print(f"ids=|{ids}|")
    for story_id in ids:
        hide_single_story(request.user.id, story_id)
    print(f"request.META.get('HTTP_REFERER')={request.META.get('HTTP_REFERER')}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def hide_story(request):
    body = json.loads(request.body)
    story_id = body["id"]
    hide = body["hide"]
    print(f'Story to hide {story_id}')
    try:
        hide_single_story(request.user.id, story_id, hide)
        return HttpResponse()
    except:
        return HttpResponse(status=400)

@login_required
def save_story(request):
    body = json.loads(request.body)
    story_id = body["id"]
    print(f'Story to save {story_id}')
    try:
        save_single_story(request.user.id, story_id)
        return HttpResponse()
    except:
        return HttpResponse(status=400)

@login_required
def delete_story(request):
    body = json.loads(request.body)
    story_id = body["id"]
    print(f'Story to delete {story_id}')
    try:
        user_story = get_object_or_404(UserStory, story_id=story_id)
        user_story.saved = False
        user_story.save()
        return HttpResponse()
    except:
        return HttpResponse(status=400)