from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from ..models import Location


@login_required(login_url="signin")
def location_index(request):
    locations = Location.objects.order_by("-id")
    paginator = Paginator(locations, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "location/index.html", {"page_object": page_object})


@login_required(login_url="signin")
def location_show(request, id):
    location = get_object_or_404(Location, pk=id)
    return render(request, "location/show.html", {"location": location})


@login_required(login_url="signin")
def location_create(request):
    if request.method == "GET":
        return render(request, "location/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        longitude = request.POST["longitude"]
        latitude = request.POST["latitude"]
        description = request.POST["description"]
        location = Location(
            name=name,
            latitude=latitude,
            longitude=longitude,
            description=description,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            location.image = request.FILES.get("image")

        location.save()
        messages.info(request, "location saved")
        return redirect("location.index")
 

@login_required(login_url="signin")
def location_edit(request, id):
    location = get_object_or_404(Location, pk=id)

    if request.method == "GET":
        return render(request, "location/edit.html", {"location": location})

    elif request.method == "POST":
        location.name = request.POST["name"]
        location.latitude = request.POST["latitude"]
        location.longitude = request.POST["longitude"]
        location.description = request.POST["description"]

        if request.FILES.get("image") != None:
            location.image = request.FILES.get("image")

        if location.user_id == request.user.id:
            location.save()
            messages.info(request, "location updated")

        return redirect("location.index")


@login_required(login_url="signin")
def location_delete(request, id):
    location = get_object_or_404(Location, pk=id)

    if location.user_id == request.user.id:
        location.delete()
        messages.info(request, "location deleted")

    return redirect("location.index")
