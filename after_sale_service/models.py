from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    image = models.ImageField()
    description = models.TextField()
    price = models.FloatField()
    tags = models.JSONField()
    partners = models.JSONField()
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    image = models.ImageField()
    description = models.TextField()
    tags = models.JSONField()
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    image = models.ImageField()
    description = models.TextField()
    tags = models.JSONField()
    partners = models.JSONField()
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
