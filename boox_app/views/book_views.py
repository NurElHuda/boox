
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib import messages
from boox_app.models import Book
from boox_app.validators import validate_data

class BookList(ListView):
    model = Book
    context_object_name = "books"


class BookCreation(View):
    def get(self, request, *args, **kwargs):
        return render(request, "boox_app/book_creation.html")

    def post(self, request, *args, **kwargs):
        fields = ["title", "author_name", "price", "goodread"]
        data, errors = validate_data(fields, request.POST)
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, "boox_app/book_creation.html", {"errors": errors})

        obj = Book.objects.create(**data, seller=request.user)
        return redirect("book-detail", pk=obj.pk)


class BookDetail(DetailView):
    model = Book
    context_object_name = "book"
