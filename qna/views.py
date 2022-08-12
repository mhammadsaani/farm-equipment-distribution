from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from .models import Question, Answer
from after_sale_service.models import Tag
from django.db.models import Q


# Create your views here.
@require_http_methods(["GET"])
def question_index(request):
    questions = Question.objects.order_by("-id")
    tags = Tag.objects.order_by("-id")[:10]
    paginator = Paginator(questions, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request, "qna/question/index.html", {"tags": tags, "page_object": page_object}
    )


# TODO: validate tags
@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def question_create(request):
    if request.method == "GET":
        tags = Tag.objects.order_by("-id")[:10]
        return render(request, "qna/question/create.html", {"tags": tags})

    elif request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        category = request.POST["category"]

        question = Question(
            title=title,
            slug=slugify(title),
            content=content,
            category_id=category,
            user_id=request.user.id,
        )

        if request.FILES.get("attachment") != None:
            question.attachment = request.FILES.get("attachment")

        question.save()
        messages.info(request, "Question saved")
        return redirect("qna:question.index")


@require_http_methods(["GET"])
def question_search(request):
    keyword = request.GET.get("keyword")
    questions = Question.objects.filter(
        Q(content__contains=keyword) | Q(title__contains=keyword)
    )
    tags = Tag.objects.order_by("-id")[:10]
    paginator = Paginator(questions, 50)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request,
        "qna/question/index.html",
        {
            "tags": tags,
            "page_object": page_object,
            "keyword": request.GET.get("keyword"),
        },
    )


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def question_edit(request, id):
    question = get_object_or_404(Question, pk=id)

    if request.method == "GET":
        tags = Tag.objects.order_by("-id")[:10]

        return render(
            request, "qna/question/edit.html", {"tags": tags, "question": question}
        )

    elif request.method == "POST":
        question.title = request.POST["title"]
        question.content = request.POST["content"]

        if request.FILES.get("attachment") != None:
            question.attachment = request.FILES.get("attachment")

        if question.user_id == request.user.id:
            question.save()
            messages.info(request, "Question updated")

        return redirect("qna:question.index")


@require_http_methods(["GET"])
@login_required(login_url="signin")
def question_delete(request, id):
    question = get_object_or_404(Question, pk=id)

    if question.user_id == request.user.id:
        question.delete()
        messages.info(request, "Question deleted")

    return redirect("qna:question.index")


@require_http_methods(["GET"])
def question_show(request, slug):
    tags = Tag.objects.order_by("-id")[:10]
    question = get_object_or_404(Question, slug=slug)
    tags_json = serialize("json", tags, fields=("name"))
    answers = Answer.objects.filter(question_id=question.id).order_by("-id")[:10]

    return render(
        request,
        "qna/question/show.html",
        {
            "tags": tags,
            "answers": answers,
            "question": question,
            "tags_json": tags_json,
        },
    )


@require_http_methods(["POST"])
@login_required(login_url="signin")
def answer_create(request):
    tags = request.POST["tags"]
    content = request.POST["content"]
    question_id = request.POST["question"]

    answer = Answer(
        tags=tags, content=content, question_id=question_id, user_id=request.user.id
    )

    if request.FILES.get("attachment") != None:
        answer.attachment = request.FILES.get("attachment")

    answer.save()
    messages.info(request, "Answer saved")
    return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET"])
@login_required(login_url="signin")
def answer_delete(request, id):
    answer = get_object_or_404(Answer, pk=id)

    if answer.user_id == request.user.id:
        answer.delete()
        messages.info(request, "Answer deleted")

    return redirect(request.META.get("HTTP_REFERER"))
