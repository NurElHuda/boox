from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.BookList.as_view(), name="home"),
    path('books/<int:pk>/', views.BookDetail.as_view(), name="book-detail")
]
