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
from .models import Exam,Question,Answer,Taghalob
from .forms import ExamCreateForm,QuestionCreateForm,NumberofQuestionForm
from django.forms import modelformset_factory
from .forms import QuestionCreateForm,AnswerForm
from accounts.models import User
class ExamCreateView(View):
    def get(self,request):
        form = ExamCreateForm()
        return render(request,"exam/create-exam.html",{'form':form})
    def post(self,request):
        form = ExamCreateForm(request.POST)
        if form.is_valid():
            exam = form.save()
            request.session["exam_id"] = exam.pk
            return redirect("exam:question-number")
        return render(request, "exam/create-exam.html", {'form': form})


class QuestionNumberView(View):
    def get(self,request):
        form = NumberofQuestionForm()
        return render(request,"exam/number-question.html",{'form':form})

    def post(self,request):
        form = NumberofQuestionForm(request.POST)
        if form.is_valid():
            number_of_question = form.cleaned_data['number_of_question']
            request.session['number_of_question'] = number_of_question
            return redirect("exam:question-create")
        return render(request,"exam/number-question.html",{'form':form})


class QuestionCreateView(View):
    def get(self, request):
        number_of_question = request.session.get('number_of_question', 1)
        QuestionFormSet = modelformset_factory(Question, form=QuestionCreateForm, extra=number_of_question)
        formset = QuestionFormSet(queryset=Question.objects.none())  # فرم‌های خالی
        return render(request, "exam/create-question.html", {'forms': formset})

    def post(self, request):
        number_of_question = request.session.get('number_of_question')
        exam_id = request.session.get('exam_id')

        QuestionFormSet = modelformset_factory(Question, form=QuestionCreateForm, extra=number_of_question)
        formset = QuestionFormSet(request.POST)

        if formset.is_valid():
            instances = formset.save(commit=False)
            exam = Exam.objects.get(pk=exam_id)
            for instance in instances:
                instance.exam = exam
                instance.save()
            return redirect("exam:question-success")
        else:
            print(formset.errors)
        return render(request, "exam/create-question.html", {'forms': formset})


class SuccessQuestionView(View):
    def get(self,request):
        return render(request,"exam/success-question.html")

class ExamSelectedView(View):
    def get(self,request):
        exams = Exam.objects.all()
        return render(request,"exam/exam-selected.html",{'exams':exams})




class QuizView(View):
    def get(self,request,pk):
        question = Question.objects.filter(exam=pk)
        return render(request,"exam/quiz.html",{'question':question})

    def post(self, request, pk):
        user_name = request.session.get('user_name')
        user = User.objects.filter(name=user_name).first()
        if not user:
            return redirect("accounts:register-user")

        for question in Question.objects.filter(exam=pk):
            answer_text = request.POST.get(f'answer_{question.id}')
            if answer_text:
                Answer.objects.create(
                    user=user,
                    question=question,
                    student_answer=answer_text,
                )
        return redirect('quiz_results')