from django.urls import path

from . import views

app_name = "customers"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("signup_request/", views.signup_request, name="signup_request"),
    path("logout/", views.logout, name="logout"),
    path("login_request/", views.login_request, name="login_request"),
    path("bookmarked/", views.bookmarked, name="bookmarked"),
]
