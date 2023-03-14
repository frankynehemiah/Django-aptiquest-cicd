import json
from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from. import forms as QFORM
from rootQuiz import models as QMODEL
from .forms import CustomQuizForm,QuestionForm
from django.shortcuts import get_object_or_404

# Create your views here.
currentQuizId = ""
def SetCurrentQuizId(x):
    global currentQuizId
    currentQuizId = x

def addQuestion(request):
    if request.user.is_authenticated:
        quizId = request.GET.get('quiz_id')
        print("this is the Quiz id:",quizId)
        SetCurrentQuizId(quizId)
        players = QMODEL.Player.objects.get(user_id = request.user.id)
        if QMODEL.CustomQuiz.objects.filter(creator =players,quizCode=currentQuizId).exists():
            customQuiz  = QMODEL.CustomQuiz.objects.get(creator =players,quizCode=currentQuizId)
            questionList = QMODEL.Question.objects.filter(quiz_id_to_store = customQuiz)

            print("This is the Questions", questionList)
        # =================================================================
        if request.method=='POST':
            questionForm=QuestionForm(request.POST)
            if questionForm.is_valid():
                question=questionForm.save(commit=False)
                if QMODEL.CustomQuiz.objects.filter(quizCode=quizId).exists():
                    print("This quiz code exisist ",QMODEL.CustomQuiz.objects.filter(quizCode=quizId))
                    question.quiz_id_to_store = QMODEL.CustomQuiz.objects.get(quizCode=quizId)
                    question.save()
                    customQuiz  = QMODEL.CustomQuiz.objects.get(creator =players,quizCode=currentQuizId)
                    questionList = QMODEL.Question.objects.filter(quiz_id_to_store = customQuiz)
                # return HttpResponseRedirect('/add_questions.html')
            else:
                print("form is invalid")
        else:
            questionForm = QuestionForm()
        return render(request,'add_questions.html',{'questionForm':questionForm,'questionList':questionList})
    else:
       return redirect('login')


def customQuiz(request):
    if request.method == 'POST':
        form = CustomQuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            player = QMODEL.Player.objects.get(user_id = request.user.id)
            quiz.creator = player  # Assign the current player as the creator
            quiz.numberOfPeopleAttempted = 0  # Set the initial number of attempts to zero
            quiz.isActive = True  # Set the quiz as active by default
            quiz.save()  # Save the quiz to the database
            # quiz_name = form.cleaned_data['quiz_name']
            # total_questions = form.cleaned_data['total_questions']
            # total_marks = form.cleaned_data['total_marks']
            # is_timed = form.cleaned_data['is_timed']
            # time = form.cleaned_data['time']
            # retest = form.cleaned_data['retest']
            # show_marks = form.cleaned_data['show_marks']
            return redirect('custom_quiz_home')
    else:
        form = CustomQuizForm()
    return render(request, 'custom_quiz.html', {'form': form})

# This is the home page to load all Custom Quizes
def customQuizHome(request):
    if request.user.is_authenticated:
        player = QMODEL.Player.objects.get(user_id = request.user.id)
        if QMODEL.CustomQuiz.objects.filter(creator = player).exists():
            getCustomQuiz = QMODEL.CustomQuiz.objects.filter(creator = player)
        else:
            getCustomQuiz = None
        # print("This is custom Quiz ",getCustomQuiz)
        return render(request, 'custom_quiz_home.html',{'player':player,'customQuiz': getCustomQuiz})
    else:
        return redirect('login')
    
def sendQuizID(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            quizID = data['quiz_id']
            data = {'quiz_id': quizID}
            query_params = '&'.join([f'{key}={value}' for key, value in data.items()])
            url = f'/add_questions?{query_params}'
            return redirect(url)
        else: 
            return JsonResponse({'error': 'Invalid method'})    
    else:
        return redirect('login')
    
def ViewQuizQestions(request):
    if request.user.is_authenticated:
        players = QMODEL.Player.objects.get(user_id = request.user.id)
        print("This is the Current QUiz", currentQuizId)

        if QMODEL.CustomQuiz.objects.filter(creator =players,quizCode=currentQuizId).exists():
            customQuiz  = QMODEL.CustomQuiz.objects.filter(creator =players,quizCode=currentQuizId)
            questionList = QMODEL.Question.objects.get(quiz_id_to_store = customQuiz)
            print("This is the Questions", questionList)
        else: 
            print("")
        return render(request,'view_Questions.html')    
    else:
        return redirect('login')
    
def delQuestion(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print("The delButton was clicked")
            data = json.loads(request.body)
            queNumber = data['questionNumber']
            print(queNumber, currentQuizId)

            players = QMODEL.Player.objects.get(user_id = request.user.id)
            if QMODEL.CustomQuiz.objects.filter(creator =players,quizCode=currentQuizId).exists():
                customQuiz  = QMODEL.CustomQuiz.objects.get(creator =players,quizCode=currentQuizId)
                if QMODEL.Question.objects.filter(qID = queNumber,quiz_id_to_store=customQuiz).exists():
                    selectedQuestion = QMODEL.Question.objects.get(qID = queNumber,quiz_id_to_store=customQuiz)
                    selectedQuestion.delete()
                    print("ITEM WAS DELETED")
            return JsonResponse({'Success': 'method'})  
        else: 
            return JsonResponse({'error': 'Invalid method'})  
    else:
        return redirect('login')