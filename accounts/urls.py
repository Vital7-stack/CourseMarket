from .views import ProfileUpdateView
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.register_view, name="signup"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("logout/", views.logout_view, name="logout"),  # <-- обязательно добавь эту строку
]