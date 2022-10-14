from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "feedback"
urlpatterns = [
    path("", RedirectView.as_view(url="form")),
    path("form", views.form_index, name="form.index"),
    path("form/create", views.form_create, name="form.create"),
    path("form/<int:id>", views.form_show, name="form.show"),
    path("form/<int:id>/edit", views.form_edit, name="form.edit"),
    path("form/<int:id>/delete", views.form_delete, name="form.delete"),
]
