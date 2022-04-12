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


def authenticate_with_google(firebase_id_token):
    try:
        credentials = verify_id_token(firebase_id_token)
        print(f"cred: {credentials}")
    except Exception as ex:
        return None, "Authentication failed"
    
    try:
        user = User.objects.get(email=credentials["email"])
        return user, None
    except User.DoesNotExist:
        return None, "No account with this email"


def login_succeeded(request, user):
    login(request, user)
    messages.success(request, 'Login successfull', extra_tags="success")
    return redirect("home")


def login_failed(request, error=None):
    if not error:
        error = 'Login failed: wrong email or password' 
    messages.error(request, error, extra_tags="danger")
    return render(request, "boox_app/sign_in.html")


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("err", None) and request.GET["err"] == '1':
            messages.error(request, request.GET.get("err_code"))
        return render(request, "boox_app/sign_up.html")

    def post(self, request, *args, **kwargs):
        data, errors = validate_data(["name", "email", "password"], request.POST)
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
        data, errors = validate_data(["email", "password", "provider", "firebase_id_token"], request.POST)

        user = authenticate(request, email=data["email"], password=data["password"])
        if user:
            return login_succeeded(request, user)
        elif "provider" in data and data["provider"] == "google" and "firebase_id_token" in data:
            user, error = authenticate_with_google(data["firebase_id_token"])
            print(f"u: {user}")
            if user:
                return login_succeeded(request, user)
            else:
                return login_failed(request, error)
        else:
            return login_failed(request)


class SignOutView(View):

    def logout(self, request):
        dj_logout(request)
        messages.success(request, 'Logout successfull. Sad to see you go.')
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return self.logout(request)

    def post(self, request, *args, **kwargs):
        return self.logout(request)
