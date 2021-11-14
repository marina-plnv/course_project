from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *


def index(request):
    movies = Movie.objects.all()
    context = {
        "movies": movies,
    }
    return render(request, 'main/index.html', context)


def details(request, id):
    movie = Movie.objects.get(id=id)
    context = {
        'movie': movie
    }
    return render(request, 'main/details.html', context)


def signin(request):
    return render(request, 'main/login.html')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            # password1 = form.cleaned_data('password1') используете ModelForm, то нет никакой необходимости играть со словарем cleaned_data
            password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('main:home')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {"form": form})
