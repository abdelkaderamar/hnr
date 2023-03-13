"""hnr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from feed import views as feedViews

from rest_framework import routers

from feed.models import *
from feed import views as feedViews
from .views import about

router = routers.DefaultRouter()
router.register(r'stories', feedViews.StoryViewSet, basename="stories")
router.register(r'best_stories', feedViews.BestStoryViewSet, basename="best_stories")
router.register(r'top_stories', feedViews.TopStoryViewSet, basename="top_stories")
router.register(r'new_stories', feedViews.NewStoryViewSet, basename="new_stories")
router.register(r'ask_stories', feedViews.AskStoryViewSet, basename="ask_stories")
router.register(r'show_stories', feedViews.ShowStoryViewSet, basename="show_stories")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', feedViews.home, name='home'),
    path('about', about, name='about'),
    path('feed/', include('feed.urls')),
    path('accounts/', include('accounts.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),

]
