from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('books/<int:pk>/', views.BookDetail.as_view(), name="book-detail")
]
