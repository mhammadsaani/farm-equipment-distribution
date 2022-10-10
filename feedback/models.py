from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Form(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class QuestionField(models.Model):
    NUMBER = "number"
    TEXT = "text"
    INPUT = "input"
    BOOL = "bool"
    DATE = "date"
    SELECT = "select"

    CHOICES = (
        (BOOL, BOOL),
        (DATE, DATE),
        (INPUT, INPUT),
        (TEXT, TEXT),
        (NUMBER, NUMBER),
        (SELECT, SELECT),
    )

    type = models.CharField(max_length=200, choices=CHOICES, default=INPUT)
    label = models.CharField(max_length=200)
    choice = models.CharField(max_length=200)
    width = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


class Response(models.Model):
    value = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionField, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.value
