from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Message(models.Model):
    content = models.TextField()
    attachment = models.FileField()
    created_at = models.DateTimeField(default=datetime.now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.IntegerField()

    def __str__(self):
        return self.content
