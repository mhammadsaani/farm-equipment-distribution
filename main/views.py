from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from django.forms.models import model_to_dict
from django.contrib import messages
from .models import Profile, Notification, Product, Location
from django.db.models import Q

# Create your views here.
@require_http_methods(["GET"])
def home(request):
    products = Product.objects.order_by("-id")[:10]
    locations = Location.objects.order_by("-id")[:10]

    return render(
        request,
        "home.html",
        {"locations": locations, "products": products},
    )


@require_http_methods(["GET"])
def profile(request, id):
    user = get_object_or_404(User, pk=id)

    if not Profile.objects.filter(profile_user_id=id).exists():
        profile = Profile.objects.create(user=user, profile_user_id=user.id)
        profile.save()
    else:
        profile = Profile.objects.filter(profile_user_id=id).get()

    return render(request, "profile.html", {"profile": profile, "user": user})


@require_http_methods(["GET"])
def apply(request):
    form = Form.objects.filter(name__icontains="apply for partnership").first()

    if form != None:
        return redirect("feedback:form.show", id=form.id)
    else:
        messages.info(request, "Page not found")
        return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET"])
def contact(request):
    pass


@require_http_methods(["GET"])
@login_required(login_url="signin")
def dashboard(request):
    product_count = Product.objects.count()
    location_count = Location.objects.count()
    notification_count = Notification.objects.count()

    return render(
        request,
        "dashboard.html",
        {
            "product_count": product_count,
            "location_count": location_count,
            "notification_count": notification_count,
        },
    )


@login_required(login_url="signin")
@require_http_methods(["GET", "POST"])
def settings(request):

    if request.method == "GET":
        settings = Settings.objects.filter(user_id=request.user.id).all()
        profile = Profile.objects.filter(profile_user_id=request.user.id).first()

        return render(
            request,
            "settings.html",
            {"settings": settings, "profile": profile},
        )


@require_http_methods(["POST"])
@login_required(login_url="signin")
def profile_update(request, id):
    user = get_object_or_404(User, pk=request.user.id)

    if not Profile.objects.filter(profile_user_id=id).exists():
        profile = Profile.objects.create(user=user, profile_user_id=user.id)
        profile.save()
    else:
        profile = Profile.objects.filter(profile_user_id=id).get()

    user.last_name = request.POST["last_name"]
    user.first_name = request.POST["first_name"]
    user.username = request.POST["username"]
    user.email = request.POST["email"]
    profile.bio = request.POST["bio"]

    if request.FILES.get("image") != None:
        profile.image = request.FILES.get("image")

    user.save()
    profile.save()
    messages.info(request, "Settings updated")

    return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET"])
@login_required(login_url="signin")
def notification(request):
    notifications = get_list_or_404(Notification, user_id=request.user.id)
    # ! show all my notifications
    return HttpResponse("Show all notifications")


@require_http_methods(["GET"])
@login_required(login_url="signin")
def notification_delete(request, id):
    notification = get_object_or_404(Notification, pk=id)
    # ! redirect user after deleting notification
    if notification.user_id == request.user.id:
        notification.delete()

    return redirect(request.META.get("HTTP_REFERER"))


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == "" or password != confirm_password:
            messages.info(request, "Password do not match")
            return redirect("signup")

        if email == "" or User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect("signup")

        if username == "" or User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("signup")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        user_model = User.objects.get(email=email)
        new_profile = Profile.objects.create(
            user=user_model, profile_user_id=user_model.id
        )
        new_profile.save()
        return redirect("dashboard")


@require_http_methods(["GET", "POST"])
def signin(request):
    if request.method == "GET":
        return render(request, "signin.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect("signin")

        auth.login(request, user)
        return redirect("dashboard")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("home")
