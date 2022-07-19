from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from .models import Question, Answer
from after_sale_service.models import Tag


# Create your views here.
@require_http_methods(["GET"])
def question_index(request):
    tags = Tag.objects.order_by("-id")[:10]
    questions = Question.objects.order_by("-id")[:10]
    return render(
        request, "qna/question/index.html", {"tags": tags, "questions": questions}
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


def question_search(request):
    pass


def question_edit(request, id):
    pass


def question_delete(request, id):
    question = get_object_or_404(Question, pk=id)
    question.delete()
    messages.info(request, "Question deleted")
    return redirect("qna:question.index")


def question_show(request, slug):
    pass


def answer_index(request):
    pass


def answer_create(request):
    pass


def answer_edit(request, id):
    pass


def answer_delete(request, id):
    pass


def answer_show(request, slug):
    pass
