from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.register_view, name="signup"),
    path("profile/", views.ProfileDetailView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile-edit"),
    path("logout/", views.logout_view, name="logout"),
]