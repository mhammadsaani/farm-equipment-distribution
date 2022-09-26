from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "feedback"
urlpatterns = [
    path("", RedirectView.as_view(url="response")),
    path("response", views.response_index, name="response.index"),
]
