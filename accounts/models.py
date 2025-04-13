from django.db import models


type_person=(
    (1,("Teacher")),
    (2,("Student"))
)

class User(models.Model):
    name = models.CharField(max_length=250)
    type = models.IntegerField(choices=type_person)

    def __str__(self):
        return f"{self.pk}-{self.name}"
