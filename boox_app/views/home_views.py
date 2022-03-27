from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required

class HomeView(View):
    greeting = "Good Day"

    @login_required
    def get(self, request):
        return render(request, 'boox_app/home.html')