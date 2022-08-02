from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from .models import Question, Answer
from after_sale_service.models import Tag


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

        if Tag.objects.filter(name=category).exists():
            tag = Tag.objects.get(name=category)
        else:
            tag = Tag(name=category, slug=slugify(category), user_id=request.user.id)
            tag.save()

        question = Question(
            title=title,
            slug=slugify(title),
            content=content,
            category_id=tag.id,
            user_id=request.user.id,
        )
        question.save()
        messages.info(request, "Question saved")
        return redirect("qna:question.index")


@require_http_methods(["GET"])
def question_search(request):
    questions = Question.objects.filter(content__contains=request.GET.get("keyword"))
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

        if question.user_id == request.user.id:
            question.save()
            messages.info(request, "Question updated")

        return redirect("qna:question.index")


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
    return render(
        request, "qna/question/show.html", {"question": question, "tags": tags}
    )


def answer_index(request):
    pass


def answer_create(request):
    pass


def answer_edit(request, id):
    pass


def answer_delete(request, id):
    pass
