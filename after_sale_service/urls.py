from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "after-sale-service"
urlpatterns = [
    path("", RedirectView.as_view(url="product")),
    path("partner", views.partner_index, name="partner.index"),
    path("partner/create", views.partner_create, name="partner.create"),
    path("partner/<int:id>/edit", views.partner_edit, name="partner.edit"),
    path("partner/<int:id>/delete", views.partner_delete, name="partner.delete"),
    path("partner/<slug:slug>", views.partner_show, name="partner.show"),
    path("product", views.product_index, name="product.index"),
    path("product/create", views.product_create, name="product.create"),
    path("product/<int:id>/edit", views.product_edit, name="product.edit"),
    path("product/<int:id>/delete", views.product_delete, name="product.delete"),
    path("product/<slug:slug>", views.product_show, name="product.show"),
    path("service", views.service_index, name="service.index"),
    path("service/create", views.service_create, name="service.create"),
    path("service/<int:id>/edit", views.service_edit, name="service.edit"),
    path("service/<int:id>/delete", views.service_delete, name="service.delete"),
    path("service/<slug:slug>", views.service_show, name="service.show"),
]
