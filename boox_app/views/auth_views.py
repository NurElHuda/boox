# from boox_app.forms.auth_forms import SignInForm
from boox_app.models import Book, User
from boox_app.validators import validate_data
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.views import View
from firebase_admin.auth import verify_id_token


def create_user(data):
    return User.objects.create(
        name=data["name"],
        email=data["email"],
        username=data["email"],
        password=make_password(data["password"]),
        is_seller=True,
    )


def authenticate_with_firebase(data):
    try:
        credentials = verify_id_token(data["firebase_id_token"])
    except Exception as ex:
        return None, "Authentication failed"

    try:
        user = User.objects.get(email=data["email"])
    except User.DoesNotExist:
        user = create_user(data)

    return user, None


def login_succeeded(request, user):
    login(request, user)
    messages.success(request, "Login successfull", extra_tags="success")
    return redirect("home")


def login_failed(request, error=None):
    if not error:
        error = "Login failed: wrong email or password"
    messages.error(request, error, extra_tags="danger")
    return render(request, "boox_app/sign_in.html")


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("err", None) and request.GET["err"] == "1":
            messages.error(request, request.GET.get("err_code"))
        return render(request, "boox_app/sign_up.html")

    def post(self, request, *args, **kwargs):
        data, errors = validate_data(request.POST)
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, "boox_app/sign_up.html", {"errors": errors})

        try:
            user = User.objects.get(email=data["email"])
            errors["email"] = "Email already exists"
        except User.DoesNotExist:
            user = User.objects.create(
                name=data["name"],
                email=data["email"],
                username=data["email"],
                password=make_password(data["password"]),
                is_seller=True,
            )

        user = authenticate(request, email=data["email"], password=data["password"])
        login(request, user)
        return redirect("home")


class SignInView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "boox_app/sign_in.html")

    def post(self, request, *args, **kwargs):
        data, errors = validate_data(request.POST)

        user = authenticate(request, email=data["email"], password=data["password"])
        if user:
            return login_succeeded(request, user)
        elif (
                data.get("provider", None) in ["google.com", "facebook.com"]
                and data.get("firebase_id_token", None)
        ):
            user, error = authenticate_with_firebase(data)
            if user:
                return login_succeeded(request, user)

        return login_failed(request, error)


class SignOutView(View):
    def logout(self, request):
        dj_logout(request)
        messages.success(request, "Logout successfull. Sad to see you go.")
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return self.logout(request)

    def post(self, request, *args, **kwargs):
        return self.logout(request)
