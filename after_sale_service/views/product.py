from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from ..models import Product, Tag


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
        return render(request, "after-sale-service/product/create.html")

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
