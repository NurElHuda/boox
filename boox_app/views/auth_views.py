import re

# from boox_app.forms.auth_forms import SignInForm
from boox_app.models import Book, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import FormView
from boox_app.validators import validate_data


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("err", None) and request.GET["err"] == '1':
            print("1.")
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
        data, errors = validate_data(["email", "password"], request.POST)
        user = authenticate(request, email=data["email"], password=data["password"])
        if user:
            login(request, user)
            messages.success(request, 'Login successfull', extra_tags="success")
            return redirect("home")
        else:
            messages.error(request, 'Login failed: wrong email or password')
            return render(request, "boox_app/sign_in.html")


class SignOutView(View):

    def logout(self, request):
        dj_logout(request)
        messages.success(request, 'Logout successfull. Sad to see you go.')
        return redirect("home")

    def get(self, request, *args, **kwargs):
        return self.logout(request)

    def post(self, request, *args, **kwargs):
        return self.logout(request)
