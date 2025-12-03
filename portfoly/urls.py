from django.urls import path
from .views.portfoly_views import index

urlpatterns = [
    path('portfoly/', index, name='index'),
]