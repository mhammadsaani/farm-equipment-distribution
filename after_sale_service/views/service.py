from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from ..models import Service, Tag


@require_http_methods(["GET"])
def service_index(request):
    services = Service.objects.order_by("-id")
    paginator = Paginator(services, 16)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request, "after-sale-service/service/index.html", {"page_object": page_object}
    )


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def service_create(request):
    if request.method == "GET":
        return render(request, "after-sale-service/service/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        tags = request.POST["tags"]
        partners = request.POST["partners"]
        description = request.POST["description"]

        service = Service(
            name=name,
            tags=tags,
            partners=partners,
            slug=slugify(name),
            description=description,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            service.image = request.FILES.get("image")

        service.save()
        messages.info(request, "Service saved")
        return redirect("after-sale-service:service.index")
