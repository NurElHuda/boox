
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import FormView
from boox_app.models import Book


class SignUpView(View):

    def get(self, request, *args, **kwargs):

        return render(request, "boox_app/sign_up.html")

    def post(self, request, *args, **kwargs):
        
        return redirect("home")

class SignInView(View):
    pass

class SignOutView(View):
    pass
