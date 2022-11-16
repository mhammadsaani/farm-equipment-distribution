import json
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    image = models.ImageField(upload_to="products", blank=True)
    description = models.TextField()
    price = models.CharField(max_length=200)
    tags = models.JSONField(blank=True)
    partners = models.JSONField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def json_tags(self):
        if self.tags:
            return json.loads(self.tags)
        return []

    def json_partners(self):
        if self.partners:
            return json.loads(self.partners)
        return []


class Partner(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    image = models.ImageField(upload_to="partners", blank=True)
    description = models.TextField(blank=True)
    tags = models.JSONField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def json_tags(self):
        if self.tags:
            return json.loads(self.tags)
        return []


class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=False)
    link = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="services", blank=True)
    description = models.TextField()
    tags = models.JSONField(blank=True)
    partners = models.JSONField(blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def json_tags(self):
        if self.tags:
            return json.loads(self.tags)
        return []

    def json_partners(self):
        if self.partners:
            return json.loads(self.partners)
        return []


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
