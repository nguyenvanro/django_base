from django.urls import path, include

app_name = "v1"

urlpatterns = [
    path("auth/", include("apps.authentication.urls")),
    path("users/", include("apps.users.urls")),
]