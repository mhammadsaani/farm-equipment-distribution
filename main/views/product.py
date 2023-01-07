from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from ..models import Product, Location


@login_required(login_url="signin")
def product_index(request):
    products = Product.objects.order_by("-id")
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "product/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def product_show(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product/show.html", {"product": product})


@login_required(login_url="signin")
def product_create(request):
    if request.method == "GET":
        return render(request, "product/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        product = Product(
            name=name, price=price, description=description, user_id=request.user.id
        )

        if request.FILES.get("image") != None:
            product.image = request.FILES.get("image")

        product.save()
        messages.info(request, "product saved")
        return redirect("product.index")


@login_required(login_url="signin")
def product_edit(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "GET":
        return render(request, "product/edit.html", {"product": product})

    elif request.method == "POST":
        product.name = request.POST["name"]
        product.price = request.POST["price"]
        product.description = request.POST["description"]

        if request.FILES.get("image") != None:
            product.image = request.FILES.get("image")

        product.save()
        messages.info(request, "product updated")
        return redirect("product.index")


@login_required(login_url="signin")
def product_delete(request, id):
    product = get_object_or_404(Product, pk=id)

    if product.user_id == request.user.id:
        product.delete()
        messages.info(request, "product deleted")

    return redirect("product.index")
