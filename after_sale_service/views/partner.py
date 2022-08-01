from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
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
    if not request.user.is_superuser:
        return redirect(request.META.get("HTTP_REFERER"))

    elif request.method == "GET":
        return render(request, "after-sale-service/partner/create.html")

    elif request.method == "POST":
        name = request.POST["name"]
        tags = request.POST["tags"]
        website = request.POST["website"]
        description = request.POST["description"]

        partner = Partner(
            name=name,
            slug=slugify(name),
            tags=tags,
            website=website,
            description=description,
            user_id=request.user.id,
        )

        if request.FILES.get("image") != None:
            partner.image = request.FILES.get("image")

        partner.save()
        messages.info(request, "Partner saved")
        return redirect("after-sale-service:partner.index")


def partner_edit(request, id):
    pass


def partner_delete(request, id):
    pass


def partner_show(request, slug):
    pass
