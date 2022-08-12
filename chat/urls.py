from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "chat"
urlpatterns = [
    path("", RedirectView.as_view(url="message")),
    path("message", views.message_index, name="message.index"),
    path("message/create", views.message_create, name="message.create"),
    path("message/<int:id>/delete", views.message_delete, name="message.delete"),
    path("message/<int:id>", views.message_show, name="message.show"),
]
