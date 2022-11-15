from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib import messages
from ..models import Partner, Tag

# Create your views here.
@require_http_methods(["GET"])
def partner_index(request):
    partners = Partner.objects.order_by("-id")
    paginator = Paginator(partners, 16)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request, "after-sale-service/partner/index.html", {"page_object": page_object}
    )


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def partner_create(request):
    if not request.user.is_superuser:  # redirect back
        return redirect(request.META.get("HTTP_REFERER"))

    elif request.method == "GET":
        tags = serialize("json", Tag.objects.all()[:50], fields=("name"))
        return render(request, "after-sale-service/partner/create.html", {"tags": tags})

    elif request.method == "POST":
        name = request.POST["name"]
        tags = request.POST["tags"]
        website = request.POST["website"]
        facebook = request.POST["facebook"]
        description = request.POST["description"]

        partner = Partner(
            name=name,
            slug=slugify(name),
            tags=tags,
            website=website,
            facebook=facebook,
            description=description,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            partner.image = request.FILES.get("image")

        partner.save()
        messages.info(request, "Partner saved")
        return redirect("after-sale-service:partner.index")


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def partner_edit(request, id):
    partner = get_object_or_404(Partner, id=id)

    if not request.user.is_superuser:
        return redirect(request.META.get("HTTP_REFERER"))

    elif request.method == "GET":
        tags = serialize("json", Tag.objects.all()[:50], fields=("name"))

        return render(
            request,
            "after-sale-service/partner/edit.html",
            {"partner": partner, "tags": tags},
        )

    elif request.method == "POST":
        partner.name = request.POST["name"]
        partner.tags = request.POST["tags"]
        partner.website = request.POST["website"]
        partner.facebook = request.POST["facebook"]
        partner.description = request.POST["description"]
        partner.slug = slugify(request.POST["name"])

        if request.FILES.get("image") != None:
            partner.image = request.FILES.get("image")

        partner.save()
        messages.info(request, "Partner updated")
        return redirect("after-sale-service:partner.show", slug=partner.slug)


def partner_delete(request, id):
    pass


@require_http_methods(["GET"])
def partner_show(request, slug):
    partner = get_object_or_404(Partner, slug=slug)

    return render(request, "after-sale-service/partner/show.html", {"partner": partner})
