from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render,redirect
import json, requests,random;
from random import shuffle;
from django.contrib import messages;
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, auth


# Create your views here.

category_keyword ={}
ansArray = []
numberOfQuestion = 3

#--------------------------------------------------------------------------------------#

def isLogedin(user):
    return user.groups.filter(name='username').exists()


def AppendCategory(val): 
  global category_keyword
  category_keyword = val
#how to remove backslash from string in python?

def QuestionDict(numb, question,answer,options):
    D = {
        "numb" : numb,
        "question" : question,
        "answer" : answer,
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
    if request.user.is_authenticated:
        trial_question = []
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
        #get random item in list?
        pushKeyWord = random.choice(category_keyword[category])
        print(pushKeyWord)
        #how to concatinate string in python
        URL = 'https://the-trivia-api.com/api/questions?categories='+pushKeyWord+'&limit='+str(numberOfQuestion)+'&difficulty=easy'
        Document = requests.get(URL)
        Json_DOC =Document.json()
        counter = 0
      
        for QueObj in Json_DOC:
            counter = counter +1
            options = []

            ans = str(QueObj['correctAnswer']).replace('\"','').replace('\\"','').replace('\'','')
            options.append(ans)
            ansArray.append(ans)
            for opt in QueObj['incorrectAnswers']:
                options.append(str(opt).replace('\\"','').replace('\"','').replace('\'',''))
            shuffle(options)
            # try_option =["A","A","B","C"]
            #how to add multiple replace in python string?
            trypass_ques = QueObj['question']
            
            que_pass = str(QueObj['question']).replace('\"','').replace('\\','').replace('\'','')
            ans_pass = str(QueObj['correctAnswer']).replace('\"','').replace('\\','').replace('\'','')
            trial_question.append(QuestionDict(counter,que_pass,ans_pass,options))
        print(trial_question)
        questions = (json.dumps(trial_question))
        
        return render(request,'quiz.html',{'category':category, 'questions':questions})
    else:
       return redirect('login')

def result(request):
    # print(request.POST)
    # return JsonResponse({'result':"request Handeled"})
    if request.method == 'POST': 
        data = json.loads(request.body)
        answers = data['ansArray']
        counter = 0
        # how to compare string in python?
        for i in range(0,numberOfQuestion):
            print(len(answers),"THis is answer length\n")
            print( len(ansArray))
            if(answers[i] == ansArray[i]):
              counter = counter + 1    
        return JsonResponse({'result': counter})
    else: 
        return JsonResponse({'error': 'Invalid method'})
    
    # LOGIN FUNCTION:

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
                user.save()
                return redirect('login')    
        else:
            messages.info(requests,"Password not same")
            return redirect('register')     
    else:
      return  render(requests, "register.html")