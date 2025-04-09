from django.db import models


type_person=(
    (1,("Teacher")),
    (2,("Student"))
)

class User(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(choices=type_person)
