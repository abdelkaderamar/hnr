from django.shortcuts import render

from .task import create_random_user_accounts
from .models import TopStory

def index(request):
    print(f"Index")
    stories = TopStory.objects.all().order_by('-time')
    context = {'stories': stories, }
    return render(request, 'feed/index.html', context)

def feed_admin(request):
    context = {}
    return render(request, 'feed/admin.html', context)

def refresh(request):
    pass

def save(request, story_id):
    print(f"Saving the story {story_id}")
    return index(request)

def sort(request, sort_param):
    if sort_param in ['score', 'descendants']:
        stories = TopStory.objects.all().order_by(f'-{sort_param}')
    elif sort_param == 'ratio':
        stories = list(TopStory.objects.all())
        stories.sort(key=lambda s : 0 if s.descendants == 0 else s.score/s.descendants, reverse=True)
    context = {'stories': stories, }
    return render(request, 'feed/index.html', context)
