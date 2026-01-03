
from django.urls import path
from apps.authentication.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
]