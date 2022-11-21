from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from ..models import Service, Tag, Partner
import json


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
        tags = serialize("json", Tag.objects.all()[:50], fields=("name"))
        partners = serialize("json", Partner.objects.all()[:50], fields=("name"))
        return render(
            request,
            "after-sale-service/service/create.html",
            {"tags": tags, "partners": partners},
        )

    elif request.method == "POST":
        name = request.POST["name"]
        link = request.POST["link"]
        tags = request.POST["tags"]
        partners = request.POST["partners"]
        description = request.POST["description"]

        service = Service(
            name=name,
            tags=tags,
            link=link,
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


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def service_edit(request, id):
    service = get_object_or_404(Service, id=id)

    if not request.user.is_superuser:
        return redirect(request.META.get("HTTP_REFERER"))

    elif request.method == "GET":
        tags = serialize("json", Tag.objects.all()[:50], fields=("name"))
        partners = serialize("json", Partner.objects.all()[:50], fields=("name"))

        return render(
            request,
            "after-sale-service/service/edit.html",
            {"tags": tags, "partners": partners, "service": service},
        )

    elif request.method == "POST":
        service.name = request.POST["name"]
        service.link = request.POST["link"]
        service.tags = request.POST["tags"]
        service.partners = request.POST["partners"]
        service.description = request.POST["description"]
        service.slug = slugify(request.POST["name"])

        if request.FILES.get("image") != None:
            service.image = request.FILES.get("image")

        service.save()
        messages.info(request, "Service updated")
        return redirect("after-sale-service:service.show", slug=service.slug)


def service_delete(request, id):
    pass


@require_http_methods(["GET"])
def service_show(request, slug):
    service = get_object_or_404(Service, slug=slug)
    partners = []
    for partner in json.loads(service.partners):
        partners.append(get_object_or_404(Partner, name=partner["value"]))

    return render(
        request,
        "after-sale-service/service/show.html",
        {"service": service, "partners": partners},
    )
