from django.shortcuts import render
from django.core.paginator import Paginator

from .task import create_random_user_accounts
from .models import TopStory

def get_stories_page(request, stories):
    paginator = Paginator(stories, 25)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    print(f"Index")
    stories = TopStory.objects.all().order_by('-time')
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
    return index(request)

def sort(request, sort_param):
    if sort_param in ['score', 'descendants']:
        stories = TopStory.objects.all().order_by(f'-{sort_param}')
    elif sort_param == 'ratio':
        stories = list(TopStory.objects.all())
        stories.sort(key=lambda s : 0 if s.descendants == 0 else s.score/s.descendants, reverse=True)
    stories_page = get_stories_page(request, stories)
    context = {'stories': stories_page, }
    return render(request, 'feed/index.html', context)
