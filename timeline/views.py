from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from .models import Article, Post
from after_sale_service.models import Tag

# Create your views here.
@require_http_methods(["GET"])
def post_index(request):
    tags = Tag.objects.all()[:10]
    posts = Post.objects.order_by("-id")
    paginator = Paginator(posts, 20)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request, "timeline/post/index.html", {"tags": tags, "page_object": page_object}
    )


@require_http_methods(["POST"])
@login_required(login_url="signin")
def post_create(request):
    tags = request.POST["tags"]
    content = request.POST["content"]
    post = Post(tags=tags, content=content, user_id=request.user.id)

    if request.FILES.get("attachment") != None:
        post.attachment = request.FILES.get("attachment")

    post.save()
    messages.info(request, "Post saved")
    return redirect("timeline:post.index")


@require_http_methods(["POST"])
@login_required(login_url="signin")
def post_edit(request, id):
    post = get_object_or_404(Post, pk=id)
    post.tags = request.POST["tags"]
    post.content = request.POST["content"]

    if request.FILES.get("attachment") != None:
        post.attachment = request.FILES.get("attachment")

    post.save()
    messages.info(request, "Post updated")
    return redirect("timeline:post.index")


@require_http_methods(["GET"])
@login_required(login_url="signin")
def post_delete(request, id):
    post = get_object_or_404(Post, pk=id)

    if post.user_id == request.user.id:
        post.delete()
        messages.info(request, "Post deleted")

    return redirect("timeline:post.index")
