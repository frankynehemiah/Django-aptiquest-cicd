from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
import requests
from . import models as MODEL
from rootQuiz import models as RMODEL
# Create your views here.

def playCustom(request):
    if not request.user.is_authenticated:
       return redirect('login')
    if request.method == "POST":
        quizCODE = request.POST.get('quizCode',False)
        if RMODEL.CustomQuiz.objects.filter(quizCode = quizCODE).exists():
            print("FOUND")
            cQuiz = RMODEL.CustomQuiz.objects.get(quizCode = quizCODE)
            questionList = RMODEL.Question.objects.filter(quiz_id_to_store = cQuiz)
            print(questionList) 
            return render(request, "quiz.html",{'questions':questionList})

        else:
            print("NOT FOUND")
            # messages.info(requests, "USER NOT REGISTERED")
            return HttpResponse({"Not Found":"YEs"})
    
        # if user is not None:
        #     auth.login(requests,user)
        #     return redirect('/')
        # else:
        #     messages.info(requests, "USER NOT REGISTERED")
        #     return redirect('login')    
    # else:
    #     return render(requests,"login.html")

