from django.shortcuts import render


def index(request):
    return render(request, 'portfoly/pages/index.html')  