from django.urls import path;
from . import views;

urlpatterns =[
    path('custom_quiz_home',views.customQuizHome, name='custom_quiz_home'),
    path('add_questions', views.addQuestion,name='add_questions'),
    path('customQuiz',views.customQuiz,name='customQuiz'),   
    path('sendDataToQuestions',views.sendQuizID, name='sendDataToQuestions'),
    path('viewQuestions', views.ViewQuizQestions,name='viewQuestions'),
    path('del_question',views.delQuestion, name='del_question'),
]