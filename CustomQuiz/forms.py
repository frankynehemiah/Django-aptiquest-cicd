from django import forms
from django.contrib.auth.models import User
from . import models
from rootQuiz import models as MODEL


class QuestionForm(forms.ModelForm):
    # courseID=forms.ModelChoiceField(queryset=MODEL.CustomQuiz.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=MODEL.Question
        fields=['marks','question','option1','option2','option3','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50, 'class': 'form-control'}),
            'option1': forms.TextInput(attrs={'class': 'form-control'}),
            'option2': forms.TextInput(attrs={'class': 'form-control'}),
            'option3': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['quiz_id_to_store','qID']
 

class CustomQuizForm(forms.ModelForm):

    class Meta:
        model = MODEL.CustomQuiz
        fields=['quiz_name','quizCode','isTimed','time','retest','showMarks']
        lables = {
            "quiz_name": "Custom Quiz Name",
            'quizCode': 'Custom Quiz Code',
            'isTimed': 'Is Timed Quiz?',
            'time': 'Time',
            'retest': 'Can Player give a Retest?',
            'showMarks': 'Can Player see Marks?',
        }
        widgets = {
            'quiz_name': forms.TextInput(attrs={'class': 'form-control '}),
            'quiz_Code': forms.TextInput(attrs={'class': 'form-control'}),
            'isTimed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'time': forms.NumberInput(attrs={'class': 'form-control'}), 
            'retest': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'showMarks': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        exclude = ['creator', 'timeCreated', 'quizId', 'numberOfPeopleAttempted']
    