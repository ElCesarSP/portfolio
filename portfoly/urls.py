from django.urls import path
from . import views

app_name = "portfoly"

urlpatterns = [
    path("", views.index, name="index"),
]
