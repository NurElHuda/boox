from django.urls import include, path

from . import views

urlpatterns = [
    path('privacy/', views.SignUpView.as_view(), name="sign-up"),

    path('sign-up/', views.SignUpView.as_view(), name="sign-up"),
    path('sign-in/', views.SignInView.as_view(), name="sign-in"),
    path('sign-out/', views.SignOutView.as_view(), name="sign-out"),
    path('', views.BookList.as_view(), name="home"),
    path('books/new/', views.BookCreation.as_view(), name="book-creation"),
    path('books/cover/', views.BookCover.as_view(), name="book-cover"),
    path('books/<int:pk>/', views.BookDetail.as_view(), name="book-detail"),
    path('books/mine/', views.BookMine.as_view(), name="book-list-mine"),

    path("update/", view=views.PullAndUpdate.as_view(), name="update"),
]

