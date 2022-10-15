from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('loginaccount',  views.loginaccount,  name='login'),
    path('logoutaccount', views.logoutaccount, name='logout'),
    path('signup', views.signup, name='signup'),
]