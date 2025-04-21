from rest_framework import serializers
from django.shortcuts import get_object_or_404
from ... models import Exam,Question,Answer


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields =["name"]

class NumberOfQuestionSerializer(serializers.Serializer):
    number_of_question = serializers.IntegerField(min_value=1)

class QuestionSerializer(serializers.ModelSerializer):
    exam = serializers.SlugRelatedField(queryset=Exam.objects.all(),slug_field="name")
    class Meta:
        model = Question
        fields = ["exam","soal","correct_answer"]

class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(queryset=Question.objects.all(),slug_field="soal")
    correct_answer = serializers.CharField(source="question.correct_answer")
    class Meta:
        model = Answer
        fields = ["user","question","student_answer","correct_answer"]