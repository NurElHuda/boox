import re

# from boox_app.forms.auth_forms import SignInForm
from boox_app.models import Book, User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import FormView
from boox_app.validators import validate_data


class SignUpView(View):
    def get(self, request, *args, **kwargs):
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
            messages.success(request, 'Login successfull')
            return redirect("home")
        else:
            messages.error(request, 'Login failed: wrong email or password')
            return render(request, "boox_app/sign_in.html")


class SignOutView(View):
    pass
