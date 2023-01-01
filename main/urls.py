from django.urls import path
from django.views.generic import TemplateView, RedirectView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", TemplateView.as_view(template_name="about.html"), name="about"),
    path("contact", views.contact, name="contact"),
    path("apply", views.apply, name="apply"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("settings", views.settings, name="settings"),
    path("notification", views.notification, name="notification"),
    path(
        "notification/<int:id>/delete",
        views.notification_delete,
        name="notification.delete",
    ),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/<int:id>/update", views.profile_update, name="profile.update"),
]
