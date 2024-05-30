from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
import json, requests,random;
from random import shuffle;
from django.contrib import messages;
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, auth
from rootQuiz import models as MODEL
from . import forms,models
from django import forms
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import date, timedelta
from django.core import serializers





# Create your views here.

category_keyword ={}
answerArray = []

checkAnswerArr = []
numberOfQuestion = 10
def setNumberOfQUestions(x):
    global numberOfQuestion
    numberOfQuestion = x

#--------------------------------------------------------------------------------------#
def isLogedin(user):
    return user.groups.filter(name='username').exists()

def setCategory(x):
  global currentCategory
  currentCategory = x
  
def AppendAnswers(val):
    global checkAnswerArr
    if(val != "" or val != None):
        checkAnswerArr.append(val)

quizIDtoPass =""

def setQuizId(x):
    global quizIDtoPass
    quizIDtoPass = x
    
def ClearAnswers():
    global checkAnswerArr
    checkAnswerArr.clear()
    print("Answer Array", checkAnswerArr)

def AppendCategory(val): 
  global category_keyword
  category_keyword = val
#how to remove backslash from string in python?

def QuestionDict(numb, question,options):
    D = {
        "numb" : numb,
        "question" : question,
        "options" : options
    } 
    return D


def home(request):
    quizCategory = []
    categoryURL = 'https://the-trivia-api.com/api/categories'
    Document = requests.get(categoryURL)
    if Document.status_code == 200:
        print("Connection SuccessFul :)")
        Djson = Document.json()
        global AppendCategory 
        AppendCategory(Djson)
                # print(Djson)
        for category in Djson:
            #how to add item in list python?
            quizCategory.append(category)
            

    else:
        print("connection failed")
    
    return render(request, 'index.html',{'quizCategory': quizCategory})

def selectedQuiz(request, category):
    trial_question = []
    counter = 0
    if request.user.is_authenticated:
        if request.method == "POST":
          quizCODE = request.POST.get('quizCode',False)
          if MODEL.CustomQuiz.objects.filter(quizCode = quizCODE).exists():
              print("FOUND")
              setCategory('customQuiz')
              setQuizId(quizCODE)
              cQuiz = MODEL.CustomQuiz.objects.get(quizCode = quizCODE)
              questionList = MODEL.Question.objects.filter(quiz_id_to_store = cQuiz)
               
              hero = serializers.serialize('json', questionList)
              
              hreoo = json.loads(hero)
              # print("THIS IS :",hreoo)
              for mdl in hreoo:
                  options = []
                  # print(mdl)
                  qq = mdl['fields']
                  counter = counter +1
                  que_pass =str(qq['question']).replace('\"','').replace('\\"','').replace('\'','')
                  options.append(str(qq['option1']).replace('\"','').replace('\\"','').replace('\'',''))
                  options.append(str(qq['option2']).replace('\"','').replace('\\"','').replace('\'',''))
                  options.append(str(qq['option3']).replace('\"','').replace('\\"','').replace('\'',''))
                  ansP = str(qq['answer']).replace('\"','').replace('\\"','').replace('\'','')
                  options.append(ansP)
                  AppendAnswers(qq['answer'])
                  setCategory(quizCODE)
                  shuffle(options)
                  trial_question.append(QuestionDict(counter,que_pass,options))
              print(trial_question)
              setNumberOfQUestions(len(trial_question))
              cQuestions = (json.dumps(trial_question))
              return render(request, "quiz.html",{'category':"Custom Quiz",'questions':cQuestions})
          else:
              return JsonResponse({"NOT FOUND"})
        
        # ==============================================Normal Code ============================
        questions_data = [
        {
        "numb": 1,
        "question": "What does HTML stand for?",
        "answer": "Hyper Text Markup Language",
        "options": [
          "Hyper Text Preprocessor",
          "Hyper Text Markup Language",
          "Hyper Text Multiple Language",
          "Hyper Tool Multi Language"
        ]
      },
        {
        "numb": 2,
        "question": "What does CSS stand for?",
        "answer": "Cascading Style Sheet",
        "options": [
          "Common Style Sheet",
          "Colorful Style Sheet",
          "Computer Style Sheet",
          "Cascading Style Sheet"
        ]
      },
        {
        "numb": 3,
        "question": "What does PHP stand for?",
        "answer": "Hypertext Preprocessor",
        "options": [
          "Hypertext Preprocessor",
          "Hypertext Programming",
          "Hypertext Preprogramming",
          "Hometext Preprocessor"
        ]
      },
        {
        'numb': 4,
        "question": "What does SQL stand for?",
        "answer": "Structured Query Language",
        "options": [
          "Stylish Question Language",
          "Stylesheet Query Language",
          "Statement Question Language",
          "Structured Query Language"
        ]
      },
        {
        "numb": 5,
        "question": "What does XML stand for?",
        "answer": "eXtensible Markup Language",
        "options": [
          "eXtensible Markup Language",
          "eXecutable Multiple Language",
          "eXTra Multi-Program Language",
          "eXamine Multiple Language"
        ]
      },
    ];
        # get random item in list?
        ClearAnswers()
        pushKeyWord = random.choice(category_keyword[category])
        print(pushKeyWord)
        #how to concatinate string in python
        URL = 'https://the-trivia-api.com/api/questions?categories='+pushKeyWord+'&limit='+str(numberOfQuestion)+'&difficulty=easy'
        Document = requests.get(URL)
        Json_DOC =Document.json()
        
      
        for QueObj in Json_DOC:
            counter = counter +1
            options = []

            ans = str(QueObj['correctAnswer']).replace('\"','').replace('\\"','').replace('\'','')
            options.append(ans)
            AppendAnswers(ans)
            for opt in QueObj['incorrectAnswers']:
                options.append(str(opt).replace('\\"','').replace('\"','').replace('\'',''))
            shuffle(options)
            # try_option =["A","A","B","C"]
            #how to add multiple replace in python string?
            trypass_ques = QueObj['question']
            
            que_pass = str(QueObj['question']).replace('\"','').replace('\\','').replace('\'','')
            ans_pass = str(QueObj['correctAnswer']).replace('\"','').replace('\\','').replace('\'','')
            trial_question.append(QuestionDict(counter,que_pass,options))
        print(trial_question)
        print(checkAnswerArr)
        questions = (json.dumps(trial_question))
        setCategory(category)
        return render(request,'quiz.html',{'category':category, 'questions':questions})
    else:
       return redirect('login')

def result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('ansArray', [])
            counter = 0
            print("Answers received:", answers)
            
            if len(answers) != len(checkAnswerArr):
                return JsonResponse({'error': 'Invalid number of answers'}, status=400)
            
            for i in range(len(answers)):
                if answers[i] == checkAnswerArr[i]:
                    counter += 1
            print("Result:", counter)

            ClearAnswers()        

            try:
                player = MODEL.Player.objects.get(user_id=request.user.id)
            except MODEL.Player.DoesNotExist:
                return JsonResponse({'error': 'Player does not exist'}, status=404)
            print("Player:", player)

            result_instance = MODEL.Result()
            print(type(result_instance))
            if currentCategory == quizIDtoPass:
                try:
                    custom_quiz = MODEL.CustomQuiz.objects.get(quizCode=quizIDtoPass)
                    result_instance.customQuizID = custom_quiz
                    result_instance.isCustom = True
                except MODEL.CustomQuiz.DoesNotExist:
                    return JsonResponse({'error': 'Custom quiz does not exist'}, status=404)

            result_instance.player = player.get_name
            result_instance.marks = int(counter)
            result_instance.category = currentCategory
            result_instance.playerIDent = player
            result_instance.save()

            print("Counter Output:", counter)
            return JsonResponse({'Marks': counter})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'error': 'An error occurred'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
    

def login(requests): 
    if requests.method == "POST":
        username = requests.POST.get('username',False)
        password = requests.POST.get('password', False)

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(requests,user)
            return redirect('/')
        else:
            messages.info(requests, "USER NOT REGISTERED")
            return redirect('login')    
    else:
        return render(requests,"login.html")

# Register user 

def register(requests):
    
    if requests.method == "POST":
        username = requests.POST.get('username', False)
        email = requests.POST.get('email', False)
        password = requests.POST.get('password', False)
        password2 = requests.POST.get('password2', False)

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(requests, "Email already Exists")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(requests, "User With this name already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                Player = MODEL.Player()
                Player.user = user
                Player.save()
                user.save()
                return redirect('login')    
        else:
            messages.info(requests,"Password not same")
            return redirect('register')     
    else:
      return  render(requests, "register.html")
    
def playerRegistration(request):
    userForm=forms.PlayerUserForm
    playerForm=forms.PlayerForm()
    mydict={'userForm':userForm,'playerForm':playerForm}
    if request.method=='POST':
        userForm=forms.PlayerUserForm(request.POST)
        playerForm=forms.PlayerForm(request.POST,request.FILES)
        if userForm.is_valid() and playerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            player=playerForm.save(commit=False)
            player.user=user
            player.save()
            my_player_group = Group.objects.get_or_create(name='PLAYER')
            my_player_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    return render(request,'PlayerSignUp.html',context=mydict)

def PlayerProfile(request):
  if request.user.is_authenticated:
    players = MODEL.Player.objects.get(user_id = request.user.id)
    if MODEL.Result.objects.filter(playerIDent=players).exists():
        Result  = MODEL.Result.objects.filter(playerIDent=players)
        print(Result)
    else:
        Result = {}
    return render(request,'player_dashboard.html',{'Result':Result})
  else:
     return redirect('login')