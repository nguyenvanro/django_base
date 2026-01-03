from django.urls import path
from apps.users.views import UserView

urlpatterns = [
    path("", UserView.as_view(), name="user"),
]