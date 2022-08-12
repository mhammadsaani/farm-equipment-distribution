from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Message
import json

# Create your views here.
@require_http_methods(["GET"])
@login_required(login_url="signin")
def message_index(request):
    users = serialize("json", User.objects.all()[:50], fields=("email"))
    messages = Message.objects.order_by("-id").filter(
        Q(receiver=request.user.id) | Q(sender_id=request.user.id)
    )

    paginator = Paginator(messages, 50)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request, "chat/message/index.html", {"users": users, "page_object": page_object}
    )


@require_http_methods(["POST"])
@login_required(login_url="signin")
def message_create(request):
    content = request.POST["content"]
    receiver = request.POST["receiver"]

    for person in json.loads(receiver):
        user = get_object_or_404(User, email=person["value"])
        message = Message(content=content, receiver=user.id, sender_id=request.user.id)

        if request.FILES.get("attachment") != None:
            message.attachment = request.FILES.get("attachment")

        message.save()

    return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET"])
@login_required(login_url="signin")
def message_delete(request, id):
    message = get_object_or_404(Message, pk=id)

    if message.sender_id == request.user.id:
        message.delete()
        messages.info(request, "Message deleted")

    return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET"])
@login_required(login_url="signin")
def message_show(request, id):
    messages = Message.objects.order_by("-id").filter(Q(receiver=id) | Q(sender_id=id))[
        :50
    ]

    return HttpResponse(serialize("json", messages), content_type="application/json")
