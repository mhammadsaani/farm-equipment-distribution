from django.shortcuts import render

# Create your views here.
def partner_index(request):
    return render(request, "after-sale-service/partner/index.html")


def partner_create(request):
    return render(request, "after-sale-service/partner/create.html")


def partner_edit(request, id):
    pass


def partner_delete(request, id):
    pass


def partner_show(request, slug):
    pass
