from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

# from .models import Question, Response
import json

# Create your views here.
def response_index(request):
    return HttpResponse("response index")


def response_create(request):
    return HttpResponse("response create")


def response_delete(request):
    return HttpResponse("response delete")


def response_show(request):
    return HttpResponse("response show")
