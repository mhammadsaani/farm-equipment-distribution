from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from .models import Article, Post

# Create your views here.
@require_http_methods(["GET"])
def post_index(request):
    posts = Post.objects.order_by("-id")
    paginator = Paginator(posts, 20)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "timeline/post/index.html", {"page_object": page_object})


@login_required(login_url="signin")
@require_http_methods(["POST"])
def post_create(request):
    name = request.POST["name"]
    description = request.POST["description"]

    post = Post(name=name, description=description, user_id=request.user.id)

    if request.FILES.get("image") != None:
        post.image = request.FILES.get("image")

    post.save()
    messages.info(request, "Post saved")
    return redirect("timeline:post.index")
