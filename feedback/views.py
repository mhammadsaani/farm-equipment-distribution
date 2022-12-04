from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from .models import QuestionField, Response, Form
from django.utils.text import slugify
from django.forms.models import model_to_dict
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
            is_required = bool(request.POST.getlist("is_required")[count])

            question_field = QuestionField(
                label=slugify(label),
                field_type=field_type,
                width=width,
                choice=choice,
                form_id=form.id,
                is_required=is_required,
                user_id=request.user.id,
            )
            question_field.save()

        messages.info(request, "Form created")
        return redirect("feedback:form.index")


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def form_edit(request, id):
    form = get_object_or_404(Form, pk=id)
    question_fields = get_list_or_404(QuestionField, form_id=id)

    if not request.user.is_superuser:
        return redirect(request.META.get("HTTP_REFERER"))

    if request.method == "GET":
        return render(
            request,
            "feedback/form/edit.html",
            {"form": form, "question_fields": question_fields},
        )

    elif request.method == "POST":
        form.name = request.POST["name"]
        form.description = request.POST["description"]

        QuestionField.objects.filter(form_id=id).delete()

        for count in range(len(request.POST.getlist("label"))):
            label = request.POST.getlist("label")[count]
            field_type = request.POST.getlist("field_type")[count]
            width = request.POST.getlist("width")[count]
            choice = request.POST.getlist("choice")[count]
            is_required = bool(request.POST.getlist("is_required")[count])

            question_field = QuestionField(
                label=slugify(label),
                field_type=field_type,
                width=width,
                choice=choice,
                form_id=form.id,
                is_required=is_required,
                user_id=request.user.id,
            )
            question_field.save()

        form.save()
        messages.info(request, "Form updated")
        return redirect("feedback:form.index")


@login_required(login_url="signin")
@require_http_methods(["GET"])
def form_delete(request, id):
    form = get_object_or_404(Form, pk=id)

    if form.user_id == request.user.id:
        form.delete()
        QuestionField.objects.filter(form_id=id).delete()
        messages.info(request, "Form deleted")

    return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET", "POST"])
def form_show(request, id):
    form = get_object_or_404(Form, pk=id)
    fields = get_list_or_404(QuestionField, form_id=id)

    if request.method == "GET":
        return render(
            request, "feedback/form/show.html", {"form": form, "fields": fields}
        )

    elif request.method == "POST":
        group_id = Response.objects.count()
        for field in fields:
            response = Response(
                value=request.POST[f"{field.label}"],
                form_id=id,
                question_id=field.id,
                group_id=group_id,
            )
            response.save()

        messages.info(request, "Feedback saved successfully")
        return redirect("feedback:form.show", id=id)
