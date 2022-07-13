from django.contrib import admin
from .models import Article, Post

# Register your models here.
admin.site.register(Post)
admin.site.register(Article)
