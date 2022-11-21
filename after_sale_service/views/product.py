from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from ..models import Product, Tag, Partner
import json


@require_http_methods(["GET"])
def product_index(request):
    products = Product.objects.order_by("-id")
    paginator = Paginator(products, 16)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request, "after-sale-service/product/index.html", {"page_object": page_object}
    )


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def product_create(request):
    if request.method == "GET":
        tags = serialize("json", Tag.objects.all()[:50], fields=("name"))
        partners = serialize("json", Partner.objects.all()[:50], fields=("name"))

        return render(
            request,
            "after-sale-service/product/create.html",
            {"tags": tags, "partners": partners},
        )

    elif request.method == "POST":
        name = request.POST["name"]
        tags = request.POST["tags"]
        price = request.POST["price"]
        partners = request.POST["partners"]
        description = request.POST["description"]

        product = Product(
            name=name,
            tags=tags,
            price=price,
            partners=partners,
            slug=slugify(name),
            description=description,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            product.image = request.FILES.get("image")

        product.save()
        messages.info(request, "Product saved")
        return redirect("after-sale-service:product.index")


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)

    if not request.user.is_superuser:
        return redirect(request.META.get("HTTP_REFERER"))

    elif request.method == "GET":
        tags = serialize("json", Tag.objects.all()[:50], fields=("name"))
        partners = serialize("json", Partner.objects.all()[:50], fields=("name"))

        return render(
            request,
            "after-sale-service/product/edit.html",
            {"product": product, "tags": tags, "partners": partners},
        )

    elif request.method == "POST":
        product.name = request.POST["name"]
        product.tags = request.POST["tags"]
        product.price = request.POST["price"]
        product.partners = request.POST["partners"]
        product.description = request.POST["description"]
        product.slug = slugify(request.POST["name"])

        if request.FILES.get("image") != None:
            product.image = request.FILES.get("image")

        product.save()
        messages.info(request, "Product updated")
        return redirect("after-sale-service:product.show", slug=product.slug)


@require_http_methods(["GET"])
@login_required(login_url="signin")
def product_delete(request, id):
    product = get_object_or_404(Product, pk=id)

    if product.user_id == request.user.id:
        product.delete()
        messages.info(request, "Product deleted")

    return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET"])
def product_show(request, slug):
    product = get_object_or_404(Product, slug=slug)
    partners = []
    for partner in json.loads(product.partners):
        partners.append(get_object_or_404(Partner, name=partner["value"]))

    return render(
        request,
        "after-sale-service/product/show.html",
        {"product": product, "partners": partners},
    )
