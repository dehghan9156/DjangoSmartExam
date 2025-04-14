from django.contrib import admin
from django.urls import path,include
from . import views


app_name="exam"
urlpatterns = [
    path("create/",views.ExamCreateView.as_view(),name='exam-create'),
    path("question/number/",views.QuestionNumberView.as_view(),name='question-number'),
    path("question/create/",views.QuestionCreateView.as_view(),name='question-create'),
    path("question/success/",views.SuccessQuestionView.as_view(),name='question-success'),
    path("selected/",views.ExamSelectedView.as_view(),name='exam-selected'),
    path("quiz/<int:pk>/",views.QuizView.as_view(),name='quiz'),
    path("quiz/result/",views.QuizResultView.as_view(),name='quiz-result'),

]