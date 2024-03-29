from django.urls import path
from . import views

app_name='feed'

urlpatterns = [
    path('', views.index, name='index'),
    path('feed_admin', views.feed_admin, name='feed_admin'),
    path('refresh', views.refresh, name='refresh'),
    path('save/<int:story_id>', views.save, name='save'),
    path('delete/<int:story_id>', views.delete, name='delete'),
    path('hide/<int:story_id>', views.hide, name='hide'),
    # path('sort/<str:sort_param>', views.sort, name='sort'),
    path('saved', views.saved, name='saved'),
    path('hidden', views.hidden, name='hidden'),
    path('top_stories', views.top_stories, name='top_stories'),
    path('best_stories', views.best_stories, name='best_stories'),
    path('new_stories', views.new_stories, name='new_stories'),
    path('ask_stories', views.ask_stories, name='ask_stories'),
    path('show_stories', views.show_stories, name='show_stories'),
    path('job_stories', views.job_stories, name='job_stories'),
    path('stories/<str:key>', views.custom_stories, name='custom_stories'),
    path('export', views.export_stories, name='export_stories'),
    path('clear_saved', views.clear_saved, name='clear_saved'),
    path('hide_story', views.hide_story, name='hide_story'),
    path('save_story', views.save_story, name='save_story'),
    path('delete_story', views.delete_story, name='delete_story'),
    path('hide_all', views.hide_all, name='hide_all'),
    path('search', views.search, name='search'),
]
