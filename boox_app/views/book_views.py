
from django.utils import timezone
from django.views.generic import DetailView, ListView

from boox_app.models import Book


class BookList(ListView):
    model = Book
    context_object_name = "books"


class BookDetail(DetailView):
    model = Book
    context_object_name = "book"
