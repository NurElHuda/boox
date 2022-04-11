
import os

from boox_app.constants import REGIONS
from boox_app.models import Book
from boox_app.validators import validate_data
from config.settings import BASE_URL, BOOK_COVERS_PATH, BOOK_COVERS_URL
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class BookList(ListView):
    model = Book
    context_object_name = "books"


class BookCreation(View):
    def get(self, request, *args, **kwargs):
        return render(request, "boox_app/book_creation.html", {"regions": REGIONS})

    def post(self, request, *args, **kwargs):
        fields = ["title", "author_name", "wilaya", "goodread", "price"]
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


class BookCover(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("file", openapi.IN_FORM, type=openapi.TYPE_FILE,),
        ],
        responses={200: "Ok", 400: "Error"},
    )
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file", None)
        if not file_obj:
            raise exceptions.ValidationError(detail={
                "file": "File not found"
            })

        if file_obj.content_type.split("/")[0] != "image":
            raise exceptions.ValidationError(detail={
                "file": "File must be an image"
            })


        fs = FileSystemStorage(location=BOOK_COVERS_PATH)
        file_name = fs.save(file_obj.name, file_obj)

        return Response({
            "file_name": file_name,
            "file_path": f"{BOOK_COVERS_URL}/{file_name}"
        }, status=200)


    parser_classes = (MultiPartParser, FormParser)
