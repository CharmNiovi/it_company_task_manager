from accounts.views import ProfileUpdateView, ProfileView, RegisterView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile_update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("<str:username>/", ProfileView.as_view(), name="profile-detail"),
]
app_name = "accounts"
