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
    LONG_TEXT = "long-text"
    BOOLEAN = "boolean"
    DATE = "date"
    SELECT = "select"

    CHOICES = (
        (BOOLEAN, BOOLEAN),
        (DATE, DATE),
        (LONG_TEXT, LONG_TEXT),
        (TEXT, TEXT),
        (NUMBER, NUMBER),
        (SELECT, SELECT),
    )

    field_type = models.CharField(max_length=200, choices=CHOICES, default=TEXT)
    label = models.CharField(max_length=200)
    choice = models.CharField(max_length=200)
    width = models.IntegerField()
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.label

    def choice_array(self):
        try:
            return self.choice.split(",")
        except:
            return []


class Response(models.Model):
    value = models.TextField()
    group_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionField, on_delete=models.CASCADE)

    def __str__(self):
        return self.value
