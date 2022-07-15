from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    bio = models.TextField()
    profile_user_id = models.BigIntegerField()
    role = models.JSONField()
    image = models.ImageField(upload_to="profiles", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    message = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    is_seen = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.message


class Settings(models.Model):
    key = models.CharField(max_length=200, unique=True)
    value = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.key


class SearchHistory(models.Model):
    keyword = models.CharField(max_length=200, unique=True)
    was_found = models.BooleanField(default=False)
    frequency = models.IntegerField(default=1)
    user_session = models.CharField(max_length=200)
    updated_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.keyword
