from django.shortcuts import render


def index(request):
    return render(request, 'places_remember/index.html')
