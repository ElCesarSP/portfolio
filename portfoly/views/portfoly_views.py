from django.contrib import messages
from django.shortcuts import redirect, render

from portfoly.forms import ContactForm
from portfoly.models import Contact, Experiment, Project, Skill, User

# Create your views here.

def index(request):
    return render(
        request, "portfoly/pages/index.html"
    )

def about(request):
    return render(
        request, "portfoly/pages/about.html"
    )