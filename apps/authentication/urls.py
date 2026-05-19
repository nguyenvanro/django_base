from django.urls import path

from .views import LoginView, LogoutView, MeView, RefreshView, VerifyView

app_name = "authentication"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify/", VerifyView.as_view(), name="verify"),
    path("me/", MeView.as_view(), name="me"),
]
