import requests
import logging
from pathlib import Path
import datetime

import django
from django.conf import settings

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
    ]
    )
    django.setup()

BASE_URL = 'https://news.ycombinator.com/item?id='

console = Console()

def get_db_story(list_type,id):
    from feed.models import Story, TopStory, BestStory, NewStory, AskStory, ShowStory, JobStory
    db_story = None
    if list_type == TOP_STORY:
        db_story = TopStory.objects.filter(id=id).first()
        if db_story is None:
            db_story = TopStory()
    elif list_type == NEW_STORY:
        db_story = NewStory.objects.filter(id=id).first()
        if db_story is None:
            db_story = NewStory()
    elif list_type == BEST_STORY:
        db_story = BestStory.objects.filter(id=id).first()
        if db_story is None:
            db_story = BestStory()
    elif list_type == ASK_STORY:
        db_story = AskStory.objects.filter(id=id).first()
        if db_story is None:
            db_story = AskStory()
    elif list_type == SHOW_STORY:
        db_story = ShowStory.objects.filter(id=id).first()
        if db_story is None:
            db_story = ShowStory()
    elif list_type == JOB_STORY:
        db_story = JobStory.objects.filter(id=id).first()
        if db_story is None:
            db_story = JobStory()
    return db_story


def fetch_stories(url: str, list_type):
    stories = requests.get(url).json()
    for story in stories:
        console.log(story)
        story_url = STORY_URL.replace('{STORY_ID}', str(story))
        json_story = requests.get(story_url).json()
        id = json_story['id']
        title = json_story['title']
        author = json_story['title']
        score = json_story['score']
        epoch = json_story['time']
        time = datetime.datetime.fromtimestamp(epoch)
        url = json_story.get('url')
        if url is None:
            url = BASE_URL + str(id)
        descendants = json_story.get('descendants')
        if descendants is None:
            descendants = 0
        
        db_story = get_db_story(list_type, id)

        if db_story.id is None:
            console.log(f"Story {json_story['title']} not found")
            db_story.id=id
            db_story.author=author
            db_story.title=title

        db_story.score = score
        db_story.url = url
        db_story.time = time
        db_story.descendants = descendants
        db_story.save()

def main():
    configure_django()
    from feed.models import Story, TopStory, BestStory, NewStory, AskStory, ShowStory, JobStory

    for cfg in ALL_STORIES_URLS:
        url = cfg[0]
        list_type = cfg[1]
        fetch_stories(url, list_type)
    # # json = requests.get(ASK_STORIES_URL).json()
    # # json = requests.get(TOP_STORIES_URL).json()
    # json = requests.get(NEW_STORIES_URL).json()
    # # inspect(json, all=True)
    # console.print(f'{len(json)} top stories')
    # top_stories=[s for s in json]
    # # console.print(top_stories)
    # count = 0
    # for db_story in top_stories:
    #     count += 1
    #     story_url = STORY_URL.replace('{STORY_ID}', str(db_story))
    #     json_story = requests.get(story_url).json()
    #     # console.print(json_story)
    #     id = json_story['id']
    #     title = json_story['title']
    #     author = json_story['title']
    #     score = json_story['score']
    #     epoch = json_story['time']
    #     time = datetime.datetime.fromtimestamp(epoch)
    #     url = json_story.get('url')
    #     # console.print(f"(1) Url = |{url}|")
    #     if url is None:
    #         url = BASE_URL + str(id)
    #     # console.print(f"(2) Url = |{url}|")
    #     descendants = json_story.get('descendants')
    #     if descendants is None:
    #         descendants = 0
    #     console.log(f"{count} {json_story['score']}|{json_story['title']}")
    #     db_story = Story.objects.filter(id=json_story['id']).first()
    #     if db_story is None:
    #         console.log(f"Story {json_story['title']} not found")
    #         story = Story(
    #             id=id,
    #             author=author,
    #             title=title,
    #             score=score,
    #             time=time,
    #             url=url,
    #             descendants=descendants
    #         )
    #         story.save()
    #     else:
    #         db_story.score = score
    #         db_story.url = url
    #         db_story.time = time
    #         db_story.descendants = descendants
    #         db_story.save()


if __name__ == '__main__':
    main()