from http.client import responses
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.generics import CreateAPIView,ListAPIView
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serialization import ExamSerializer,NumberOfQuestionSerializer,QuestionSerializer,AnswerSerializer
from ... models import Exam,Question,Answer
from difflib import SequenceMatcher



class ExamListCreateApiView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminUser]

class QuestionNumberApiView(APIView):
    def post(self, request):
        print(request.data)  # چاپ داده‌های دریافتی
        serializer = NumberOfQuestionSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data["number_of_question"]
            request.session["number_of_question"] = number
            return Response({"message": "Number question saved"}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)  # چاپ خطاهای سریالایزر
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminUser]

class QuizApiView(APIView):
    def get(self,request,pk):
        quiz = Question.objects.filter(exam=pk)
        serializer = QuestionSerializer(quiz,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class QuizAnswerApiView(APIView):
    def get(self,request,pk):
        answer = Answer.objects.filter(question__exam=pk)
        data =[]
        for ans in answer:
            similarity = SequenceMatcher(None, ans.student_answer, ans.question.correct_answer).ratio()
            item = AnswerSerializer(ans).data
            item["similarity"] = similarity
            data.append(item)
        return Response(data,status=status.HTTP_200_OK)