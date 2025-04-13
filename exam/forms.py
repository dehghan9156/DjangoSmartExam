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
        fields = ["soal","correct_answer"]
        widgets ={
            "soal":forms.TextInput(attrs={
                'class':'form-control',
            }),
            "correct_answer":forms.TextInput(attrs={
                'class':'form-control',
            })
        }

class NumberofQuestionForm(forms.Form):
    number_of_question = forms.IntegerField(min_value=1,widget=forms.NumberInput(attrs={'class': 'form-control'}))
