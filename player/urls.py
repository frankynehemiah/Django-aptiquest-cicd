from django.urls import path;
from . import views;

urlpatterns =[

path('playCustom', views.playCustom , name='playCustom'),

]