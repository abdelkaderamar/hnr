from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('loginaccount',  views.loginaccount,  name='login'),
    path('logoutaccount', views.logoutaccount, name='logout'),
    path('signup', views.signup, name='signup'),
    path('profile', views.user_profile, name='user_profile'),
    path('save_profile', views.save_profile, name='save_profile'),
]