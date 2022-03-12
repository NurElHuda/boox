from django.utils import timezone
from django.views.generic.detail import DetailView

from boox_app.models import Book

class BookDetail(DetailView):

    model = Book
