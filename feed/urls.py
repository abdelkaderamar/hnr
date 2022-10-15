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
    path('sort/<str:sort_param>', views.sort, name='sort'),
    path('sabed', views.saved, name='saved'),
]
