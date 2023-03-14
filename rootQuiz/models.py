from django.db import models
from django.contrib.auth.models import User
import uuid



class Player(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='static/images/profile_pic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=10,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
    



# QUIZ DATABASE

class CustomQuiz(models.Model): 
   creator  = models.ForeignKey(Player,on_delete=models.CASCADE)
   timeCreated = models.DateTimeField(auto_now=True)
   quizId = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
   quizCode = models.CharField(max_length=10)
   quiz_name = models.CharField(max_length=50)
   total_Questions = models.PositiveIntegerField(default=1)
   total_marks = models.PositiveIntegerField(default=1)
   isTimed = models.BooleanField()
   time = models.PositiveIntegerField()
   isActive = models.BooleanField()
   retest = models.BooleanField()
   showMarks = models.BooleanField()
   numberOfPeopleAttempted = models.PositiveIntegerField()

   def __str__(self):
        return self.quiz_name

class Question(models.Model):
    quiz_id_to_store=models.ForeignKey(CustomQuiz,on_delete=models.CASCADE)
     #refactor the name course to QuizID to add questions to perticular quiz only
    qID = models.AutoField(primary_key=True)
    marks=models.PositiveIntegerField(default=1)
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    answer=models.CharField(max_length=200)
    
    

class Result(models.Model):
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    isCustom = models.BooleanField(default=False)
    # quizID = models.ForeignKey(CustomQuiz,on_delete=models.CASCADE)  
    category = models.CharField(max_length=25)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)