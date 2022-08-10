from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "timeline"
urlpatterns = [
    path("", RedirectView.as_view(url="post")),
    path("post", views.post_index, name="post.index"),
    path("post/create", views.post_create, name="post.create"),
    path("post/<int:id>/edit", views.post_edit, name="post.edit"),
    path("post/<int:id>/delete", views.post_delete, name="post.delete"),
]
