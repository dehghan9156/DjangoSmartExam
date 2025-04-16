from django.db.models.expressions import result
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Exam, Question, Answer, Taghalob
from .forms import ExamCreateForm, QuestionCreateForm, NumberofQuestionForm
from django.forms import modelformset_factory
from .forms import QuestionCreateForm, AnswerForm
from accounts.models import User
from difflib import SequenceMatcher
from rapidfuzz import fuzz
from django.db.models import Q


class ExamCreateView(View):
    def get(self, request):
        form = ExamCreateForm()
        return render(request, "exam/create-exam.html", {'form': form})

    def post(self, request):
        form = ExamCreateForm(request.POST)
        if form.is_valid():
            exam = form.save()
            request.session["exam_id"] = exam.pk
            return redirect("exam:question-number")
        return render(request, "exam/create-exam.html", {'form': form})


class QuestionNumberView(View):
    def get(self, request):
        form = NumberofQuestionForm()
        return render(request, "exam/number-question.html", {'form': form})

    def post(self, request):
        form = NumberofQuestionForm(request.POST)
        if form.is_valid():
            number_of_question = form.cleaned_data['number_of_question']
            request.session['number_of_question'] = number_of_question
            return redirect("exam:question-create")
        return render(request, "exam/number-question.html", {'form': form})


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
    def get(self, request):
        return render(request, "exam/success-question.html")


class ExamSelectedView(View):
    def get(self, request):
        exams = Exam.objects.all()
        return render(request, "exam/exam-selected.html", {'exams': exams})


class QuizView(View):
    def get(self, request, pk):
        question = Question.objects.filter(exam=pk)
        return render(request, "exam/quiz.html", {'question': question})

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
        return redirect('exam:quiz-result')


class QuizResultView(View):
    def get(self, request):
        user_name = request.session.get('user_name')
        user = User.objects.filter(name=user_name).first()
        result = []
        answers = Answer.objects.filter(user=user)
        for ans in answers:
            similarity = SequenceMatcher(None, ans.student_answer, ans.question.correct_answer).ratio()
            result.append({
                "question": ans.question.soal,
                "student_answer": ans.student_answer,
                "correct_answer": ans.question.correct_answer,
                "similarity": round(similarity * 100),
            })
        return render(request, "exam/quiz-result.html", {'result': result})


class TaghalobStatusView(View):
    def get(self, request):
        exam_id = request.session.get('exam_id')
        exam = Exam.objects.get(pk=exam_id)
        questions = Question.objects.filter(exam=exam)
        taghalob_list = []
        for ques in questions:
            answers = Answer.objects.filter(question=ques)
            print(f"Question {ques.id} has {len(answers)} answers.")  # تعداد پاسخ‌ها را چاپ کنید

            for i in range(len(answers)):
                for j in range(i + 1, len(answers)):
                    similarity = fuzz.ratio(answers[i].student_answer, answers[j].student_answer)
                    print(f"Comparing answer {i} and {j} with similarity {similarity}%")  # چاپ شباهت‌ها

                    is_checking = similarity > 85
                    already_exist = Taghalob.objects.filter(
                        exam=exam,
                        question=ques
                    ).filter(
                        Q(student_1=answers[i].user, student_2=answers[j].user) |
                        Q(student_1=answers[j].user, student_2=answers[i].user)
                    ).exists()
                    print(f"Already exists: {already_exist}")  # چاپ نتیجه بررسی وجود داده مشابه

                    if not already_exist and similarity > 85:
                        taghalob = Taghalob.objects.create(
                            exam=exam,
                            question=ques,
                            student_1=answers[i].user,
                            student_2=answers[j].user,
                            similarity_percentage=similarity,
                            is_checking=is_checking,
                        )
                        taghalob_list.append(taghalob)
                    else:
                        taghalob = Taghalob.objects.filter(exam=exam,question=ques,student_1=answers[i].user,student_2=answers[j].user).first()
                        if taghalob:
                            taghalob_list.append(taghalob)
        return render(request, "exam/taghalob-status.html", {"taghalob_list": taghalob_list})
