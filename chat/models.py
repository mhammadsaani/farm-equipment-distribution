from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from after_sale_service.models import Tag

User = get_user_model()

# Create your models here.
class Message(models.Model):
    content = models.TextField()
    attachment = models.FileField()
    created_at = models.DateTimeField(default=datetime.now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.IntegerField()
    group = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
