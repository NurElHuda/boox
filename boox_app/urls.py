from django.urls import include, path

from . import views

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name="sign-up"),
    path('sign-in/', views.SignInView.as_view(), name="sign-in"),
    path('sign-out/', views.SignOutView.as_view(), name="sign-out"),
    path('', views.BookList.as_view(), name="home"),
    path('books/<int:pk>/', views.BookDetail.as_view(), name="book-detail")
]
