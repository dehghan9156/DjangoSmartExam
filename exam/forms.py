from django import forms
from django.forms.models import ModelForm
from .models import Exam,Question

class ExamCreateForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["name"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["exam","soal","correct_answer"]
        widgets ={
            "exam": forms.Select(attrs={
                'class': 'form-control',
            }),
            "soal":forms.TextInput(attrs={
                'class':'form-control',
            }),
            "correct_answer":forms.TextInput(attrs={
                'class':'form-control',
            })
        }

class NumberofQuestionForm(forms.ModelForm):
    number_of_question = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of questions'}))
