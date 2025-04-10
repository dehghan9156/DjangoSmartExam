from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Exam,Question
from .forms import ExamCreateForm,QuestionCreateForm,NumberofQuestionForm

class ExamCreateView(CreateView):
    model = Exam
    form_class = ExamCreateForm
    success_url = reverse_lazy("exam:question-create")
    template_name = "exam/create-exam.html"


class QuestionNumberView(View):
    def get(self,request):
        form = NumberofQuestionForm()
        return render(request,"exam/number-question.html",{'form':form})

    def post(self,request):
        pass



class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionCreateForm
    success_url = reverse_lazy("exam:question-success")
    template_name = "exam/create-question.html"

class SuccessQuestionView(View):
    def get(self,request):
        return render(request,"exam/success-question.html")