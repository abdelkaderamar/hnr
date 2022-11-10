import requests
import argparse
from pathlib import Path
import datetime
from datetime import datetime, timedelta

import django
from django.conf import settings
from django.db.models import Q

from rich import inspect
from rich.console import Console

TOP_STORY = 1
BEST_STORY = 2
NEW_STORY = 3
ASK_STORY = 4
SHOW_STORY = 5
JOB_STORY = 6

TOP_STORIES_URL  = ('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty',  TOP_STORY)
NEW_STORIES_URL  = ('https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty' , NEW_STORY)
BEST_STORIES_URL = ('https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty', BEST_STORY)
ASK_STORIES_URL  = ('https://hacker-news.firebaseio.com/v0/askstories.json?print=pretty',  ASK_STORY)
SHOW_STORIES_URL = ('https://hacker-news.firebaseio.com/v0/showstories.json?print=pretty', SHOW_STORY)
JOB_STORIES_URL  = ('https://hacker-news.firebaseio.com/v0/jobstories.json?print=pretty',  JOB_STORY)

ALL_STORIES_URLS = {
    TOP_STORIES_URL,
    NEW_STORIES_URL,
    BEST_STORIES_URL,
    ASK_STORIES_URL,
    SHOW_STORIES_URL,
    JOB_STORIES_URL
}
STORY_URL = 'https://hacker-news.firebaseio.com/v0/item/{STORY_ID}.json?print=pretty'

def configure_django():
    BASE_DIR = Path(__file__).resolve().parent.parent
    settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    },
    INSTALLED_APPS=[
        'feed.apps.FeedConfig',
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ]
    )
    django.setup()

BASE_URL = 'https://news.ycombinator.com/item?id='

console = Console()

def get_db_story(list_type,id):
    from feed.models import Story
    # from feed.models import Story, TopStory, BestStory, NewStory, AskStory, ShowStory, JobStory
    db_story = None
    if list_type == TOP_STORY:
        db_story = Story.objects.filter(id=id).first()
        if db_story is None:
            db_story = Story()
    elif list_type == NEW_STORY:
        db_story = Story.objects.filter(id=id).first()
        if db_story is None:
            db_story = Story()
    elif list_type == BEST_STORY:
        db_story = Story.objects.filter(id=id).first()
        if db_story is None:
            db_story = Story()
    elif list_type == ASK_STORY:
        db_story = Story.objects.filter(id=id).first()
        if db_story is None:
            db_story = Story()
    elif list_type == SHOW_STORY:
        db_story = Story.objects.filter(id=id).first()
        if db_story is None:
            db_story = Story()
    elif list_type == JOB_STORY:
        db_story = Story.objects.filter(id=id).first()
        if db_story is None:
            db_story = Story()
    return db_story


def fetch_stories(url: str, list_type):
    stories = requests.get(url).json()
    # for story in stories[:2]:
    for story in stories:
        # console.log(story)
        if story is None:
            continue
        story_url = STORY_URL.replace('{STORY_ID}', str(story))
        json_story = requests.get(story_url).json()
        id = json_story['id']
        title = json_story['title']
        author = json_story['title']
        score = json_story['score']
        epoch = json_story['time']
        time = datetime.fromtimestamp(epoch)
        url = json_story.get('url')
        if url is None:
            url = BASE_URL + str(id)
        descendants = json_story.get('descendants')
        if descendants is None:
            descendants = 0
        
        db_story = get_db_story(list_type, id)

        if db_story.id is None:
            console.log(f"[red]Adding[/red] [blue]{id}[/blue] {title}")
            db_story.id=id
            db_story.author=author
            db_story.title=title

        db_story.score = score
        db_story.url = url
        db_story.time = time
        db_story.descendants = descendants

        if list_type == TOP_STORY:
            db_story.is_top = True
        elif list_type == NEW_STORY:
            db_story.is_new = True
        elif list_type == BEST_STORY:
            db_story.is_best = True
        elif list_type == ASK_STORY:
            db_story.is_ask = True
        elif list_type == SHOW_STORY:
            db_story.is_show = True
        elif list_type == JOB_STORY:
            db_story.is_job = True
        db_story.save()

def import_stories():
    for cfg in ALL_STORIES_URLS:
        url = cfg[0]
        list_type = cfg[1]
        fetch_stories(url, list_type)

def parse_arguments():
    parser = argparse.ArgumentParser(description='HN utility program')
    parser.add_argument('--import', '-i', default=True, action='store_true', dest='import_stories', help='Import HN stories')
    parser.add_argument('--clean', '-c', default=False, action='store_true', dest='clean', help='Clean old stories')
    args = parser.parse_args()
    return args

def clean_stories():
    from feed.models import Story, UserStory
    now = datetime.now()
    old_date = now - timedelta(days=7)
    old_stories = Story.objects.filter(time__lt=old_date).order_by('time')
    for s in old_stories:
        saved_user_stories = UserStory.objects.filter(Q(story_id=s.id) & Q(saved=True))
        # inspect(saved_user_stories, all=True)
        if (saved_user_stories.count() == 0):
            console.print(f"The story {s.title} will be [red]deleted[/red]")
            UserStory.objects.filter(story_id=s.id).delete()
            s.delete()
        else:
            console.print(f"The story {s.title} is saved {saved_user_stories.count()} times")
def main():
    configure_django()
    # from feed.models import Story 
    args = parse_arguments()
    console.print(args)

    # from feed.models import Story , TopStory, BestStory, NewStory, AskStory, ShowStory, JobStory

    if args.import_stories:
        import_stories()
    if args.clean:
        clean_stories()

if __name__ == '__main__':
    main()