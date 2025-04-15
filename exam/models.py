from django.db import models
from accounts.models import User


class Exam(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.pk}-{self.name}"

class Question(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    soal = models.TextField()
    correct_answer = models.TextField()

    def __str__(self):
        return f"{self.pk}"

class Answer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    student_answer = models.TextField()

    def __str__(self):
        return f"{self.pk}-{self.user.name}"

class Taghalob(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,null=True)
    student_1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name="answer_student_1")
    student_2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name="answer_student_2")
    similarity_percentage = models.PositiveIntegerField(default=0)
    is_checking = models.BooleanField()

    def __str__(self):
        return f"{self.student_1}-{self.student_2}"



