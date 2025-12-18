from django.urls import path

from . import views

app_name = "portfoly"

urlpatterns = [

    # Public pages
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("projects/", views.project, name="projects"),
    path("contact/", views.contact, name="contact"),        
]