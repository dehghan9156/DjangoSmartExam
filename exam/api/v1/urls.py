from django.contrib import admin
from django.urls import path,include
from . import views

app_name="api-v1"
urlpatterns = [
    path("exam/list/create/",views.ExamListCreateApiView.as_view(),name="exam-list-create-api"),
    path("question/number/",views.QuestionNumberApiView.as_view(),name="question-number-api"),
    path("question/list/create/",views.QuestionListCreateView.as_view(),name="question-list-create-api"),
    # show question quiz based on exam
    path("quiz/<int:pk>/",views.QuizApiView.as_view(),name="quiz-api"),
    path("quiz/answer/<int:pk>/",views.QuizAnswerApiView.as_view(),name="quiz-answer-api"),


    ]