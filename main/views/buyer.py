from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from ..models import Product, Supplier, Buyer
import pandas as pd


def buyer_index(request):
    buyers = Buyer.objects.order_by("-id")
    paginator = Paginator(buyers, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "buyer/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def buyer_show(request, id):
    buyer = get_object_or_404(Buyer, pk=id)
    return render(request, "buyer/show.html", {"buyer": buyer})


@login_required(login_url="signin")
def buyer_create(request):
    if request.method == "GET":
        return render(request, "buyer/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        buyer = Buyer(
            name=name, price=price, description=description, user_id=request.user.id
        )

        if request.FILES.get("image") != None:
            buyer.image = request.FILES.get("image")

        buyer.save()
        messages.info(request, "buyer saved")
        return redirect("buyer.index")


@login_required(login_url="signin")
def buyer_edit(request, id):
    buyer = get_object_or_404(Buyer, pk=id)

    if request.method == "GET":
        return render(request, "buyer/edit.html", {"buyer": buyer})

    elif request.method == "POST":
        buyer.name = request.POST["name"]
        buyer.price = request.POST["price"]
        buyer.description = request.POST["description"]

        if request.FILES.get("image") != None:
            buyer.image = request.FILES.get("image")

        buyer.save()
        messages.info(request, "buyer updated")
        return redirect("buyer.index")


@login_required(login_url="signin")
def buyer_delete(request, id):
    buyer = get_object_or_404(Buyer, pk=id)

    if buyer.user_id == request.user.id:
        buyer.delete()
        messages.info(request, "buyer deleted")

    return redirect("buyer.index")
