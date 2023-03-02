from django.urls import path;
from . import views;

urlpatterns =[
    path('',views.home, name='home'),
    path('quiz/<str:category>', views.selectedQuiz, name='quiz'),
    path('result', views.result , name='result'),
    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('registration',views.playerRegistration, name='registration'),
     path('profile', views.PlayerProfile, name='profile'),

]