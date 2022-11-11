from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import QuestionField, Response, Form
import json

# Create your views here.
@login_required(login_url="signin")
@require_http_methods(["GET"])
def form_index(request):
    forms = Form.objects.order_by("-id")
    paginator = Paginator(forms, 20)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "feedback/form/index.html", {"page_object": page_object})


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def form_create(request):
    if request.method == "GET":
        return render(request, "feedback/form/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]

        form = Form(name=name, description=description, user_id=request.user.id)
        form.save()

        for count in range(len(request.POST.getlist("label"))):
            label = request.POST.getlist("label")[count]
            field_type = request.POST.getlist("field_type")[count]
            width = request.POST.getlist("width")[count]
            choice = request.POST.getlist("choice")[count]

            question_field = QuestionField(
                label=label,
                field_type=field_type,
                width=width,
                choice=choice,
                form_id=form.id,
                user_id=request.user.id,
            )
            question_field.save()

        messages.info(request, "Form created")
        return redirect("feedback:form.index")


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def form_edit(request, id):
    return HttpResponse("form edit")


@login_required(login_url="signin")
@require_http_methods(["GET"])
def form_delete(request, id):
    return HttpResponse("form delete")


@require_http_methods(["GET"])
def form_show(request, id):
    return HttpResponse("form show")
