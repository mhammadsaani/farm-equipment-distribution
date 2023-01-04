from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages


@login_required(login_url="signin")
def product_index(request):
    pass


@login_required(login_url="signin")
def product_show(request, id):
    pass


@login_required(login_url="signin")
def product_create(request):
    pass


@login_required(login_url="signin")
def product_edit(request, id):
    pass


@login_required(login_url="signin")
def product_delete(request, id):
    pass
