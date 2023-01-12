from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from ..models import Product, Supplier
import pandas as pd


def supplier_index(request):
    suppliers = Supplier.objects.order_by("-id")
    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "supplier/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def supplier_show(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    return render(request, "supplier/show.html", {"supplier": supplier})


@login_required(login_url="signin")
def supplier_create(request):
    if request.method == "GET":
        return render(request, "supplier/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        contact_info = request.POST["contact_info"]
        description = request.POST["description"]
        supplier = Supplier(
            name=name,
            contact_info=contact_info,
            description=description,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            supplier.image = request.FILES.get("image")

        supplier.save()
        messages.info(request, "supplier saved")
        return redirect("supplier.index")


@login_required(login_url="signin")
def supplier_edit(request, id):
    supplier = get_object_or_404(Supplier, pk=id)

    if request.method == "GET":
        return render(request, "supplier/edit.html", {"supplier": supplier})

    elif request.method == "POST":
        supplier.name = request.POST["name"]
        supplier.contact_info = request.POST["contact_info"]
        supplier.description = request.POST["description"]

        if request.FILES.get("image") != None:
            supplier.image = request.FILES.get("image")

        supplier.save()
        messages.info(request, "supplier updated")
        return redirect("supplier.index")


@login_required(login_url="signin")
def supplier_delete(request, id):
    supplier = get_object_or_404(Supplier, pk=id)

    if supplier.user_id == request.user.id:
        supplier.delete()
        messages.info(request, "supplier deleted")

    return redirect("supplier.index")
