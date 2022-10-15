from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect

from rich import inspect

from .task import create_random_user_accounts
from .models import Story, UserStory

from dataclasses import dataclass

@dataclass
class user_story_data:
    story: Story
    saved: bool = False
    ignored: bool = False

def get_stories_page(request, stories):
    paginator = Paginator(stories, 25)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def fill_user_data(stories, user, include_ignored=False):
    if not user.is_authenticated:
        return [s for s in stories.values()]
    user_stories = UserStory.objects.filter(user_id=user.id)
    print(len(user_stories))
    for us in user_stories:
        print(f"checking {us.story_id}")
        if us.story_id in stories:
            print(us.saved)
            stories[us.story_id].saved = us.saved
            stories[us.story_id].ignored = us.ignored
    if not include_ignored:
        return [s for s in stories.values() if s.ignored == False]
    return [s for s in stories.values()]

def home(request):
    return redirect('feed:index')

def index(request):
    all_stories = Story.objects.all().order_by('-time')
    stories = dict((s.id, user_story_data(s)) for s in all_stories)
    stories = fill_user_data(stories, request.user)
    stories_page = get_stories_page(request, stories)
    context = {'stories': stories_page, }
    return render(request, 'feed/index.html', context)

def feed_admin(request):
    context = {}
    return render(request, 'feed/admin.html', context)

def refresh(request):
    pass

def save(request, story_id):
    print(f"Saving the story {story_id}")
    saved_story = UserStory.objects.filter(Q(story_id=story_id) & Q(user_id=request.user.id)).first()
    if saved_story is None:
        saved_story = UserStory()
        saved_story.story_id=int(story_id)
        saved_story.user_id=request.user.id
        saved_story.saved=True
        saved_story.ignored=False
    else:
        saved_story.saved = True
    saved_story.save()
    # return redirect("feed:index")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete(request, story_id):
    print(f"Deleting the story {story_id}")
    user_story = get_object_or_404(UserStory, story_id=story_id)
    user_story.saved = False
    user_story.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect("feed:index")

def hide(request, story_id):
    print(f"Hiding the story {story_id}")
    saved_story = UserStory.objects.filter(Q(story_id=story_id) & Q(user_id=request.user.id)).first()
    if saved_story is None:
        saved_story = UserStory()
        saved_story.story_id=int(story_id)
        saved_story.user_id=request.user.id
        saved_story.saved=False
        saved_story.ignored=True
    else:
        saved_story.ignored = not saved_story.ignored
    saved_story.save()    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect("feed:index")

def sort(request, sort_param):
    if sort_param in ['score', 'descendants']:
        all_stories = Story.objects.all().order_by(f'-{sort_param}')
    elif sort_param == 'ratio':
        all_stories = list(Story.objects.all())
        all_stories.sort(key=lambda s : 0 if s.descendants == 0 else s.score/s.descendants, reverse=True)
    stories = dict((s.id, user_story_data(s)) for s in all_stories)
    stories = fill_user_data(stories, request.user)        
    stories_page = get_stories_page(request, stories)
    context = {'stories': stories_page, }
    return render(request, 'feed/index.html', context)

def saved(request):
    all_stories = UserStory.objects.filter(Q(user_id=request.user.id) &
            Q(saved=1))
    stories = dict((story.id, story) for story in all_stories)
    stories = fill_user_data(stories, request.user, include_ignored=True)        
    stories_page = get_stories_page(request, stories)
    context = {'stories': stories_page, }
    return render(request, 'feed/saved_stories.html', context)
