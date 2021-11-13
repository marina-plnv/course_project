from django.shortcuts import render
from .models import *

def index(request):
    movies = Movie.objects.all()
    context={
        "movies": movies,
    }
    return  render(request, 'main/index.html', context)

def details(request, id):
    movie=Movie.objects.get(id=id)
    context={
        'movie': movie
    }
    return render(request, 'main/details.html', context)