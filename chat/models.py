from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from after_sale_service.models import Tag

User = get_user_model()

# Create your models here.
class Message(models.Model):
    content = models.TextField()
    attachment = models.FileField(upload_to="messages/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.IntegerField()

    def __str__(self):
        return self.content

    def receiver_email(self):
        return User.objects.get(id=self.receiver).email
