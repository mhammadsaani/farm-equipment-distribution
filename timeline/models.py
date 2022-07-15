from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
from after_sale_service.models import Tag

User = get_user_model()

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    content = models.TextField()
    attachment = models.FileField(upload_to="articles/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField()
    attachment = models.FileField(upload_to="posts/%Y/%m/%d/", blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.IntegerField(default=0)
    tags = models.JSONField()

    def __str__(self):
        return self.content
