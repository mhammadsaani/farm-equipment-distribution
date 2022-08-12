from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from .models import Message

# Create your views here.
def message_index(request):
    users = User.objects.all()[:50]
    return render(request, "chat/message/index.html", {"users": users})


def message_create(request):
    pass


def message_delete(request, id):
    pass


def message_show(request, id):
    pass
