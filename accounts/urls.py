from django.urls import path
from accounts.views import RegisterView, ProfileView, ProfileUpdateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile_update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("<str:username>/", ProfileView.as_view(), name="profile-detail"),
]
app_name = "accounts"
