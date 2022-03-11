from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

class HomeView(View):
    greeting = "Good Day"

    def get(self, request):
        return render(request, 'boox_app/home.html')