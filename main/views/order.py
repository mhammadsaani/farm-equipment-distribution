from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from ..models import Product, Location, Order, Guarantee, Insurance, Buyer
import pandas as pd


@login_required(login_url="signin")
def order_index(request):
    orders = Order.objects.order_by("-id")
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "order/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def order_show(request, id):
    order = get_object_or_404(Order, pk=id)
    return render(request, "order/show.html", {"order": order})


@login_required(login_url="signin")
def order_create(request):
    if request.method == "GET":
        buyers = Buyer.objects.all()
        products = Product.objects.all()
        locations = Location.objects.all()
        insurances = Insurance.objects.all()
        return render(
            request,
            "order/create.html",
            {
                "products": products,
                "insurances": insurances,
                "locations": locations,
                "buyers": buyers,
            },
        )

    elif request.method == "POST":
        product = request.POST["product"]
        location = request.POST["location"]
        quantity = request.POST["quantity"]
        description = request.POST["description"]
        order_type = request.POST["order_type"]
        order = Order(
            product_id=product,
            location_id=location,
            quantity=quantity,
            description=description,
            order_type=order_type,
            user_id=request.user.id,
        )
        order.save()
        messages.info(request, "order saved")
        return redirect("order.index")


@login_required(login_url="signin")
def order_edit(request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == "GET":
        buyers = Buyer.objects.all()
        products = Product.objects.all()
        locations = Location.objects.all()
        insurances = Insurance.objects.all()

        return render(
            request,
            "order/edit.html",
            {
                "order": order,
                "products": products,
                "insurances": insurances,
                "locations": locations,
                "buyers": buyers,
            },
        )

    elif request.method == "POST":
        order.product_id = request.POST["product"]
        order.location_id = request.POST["location"]
        order.quantity = request.POST["quantity"]
        order.description = request.POST["description"]
        order.order_type = request.POST["order_type"]

        order.save()
        messages.info(request, "order updated")
        return redirect("order.index")


@login_required(login_url="signin")
def order_delete(request, id):
    order = get_object_or_404(Order, pk=id)

    if order.user_id == request.user.id:
        order.delete()
        messages.info(request, "order deleted")

    return redirect("order.index")
