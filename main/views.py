from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *


def index(request):
    catalog_items = CatalogItem.objects.all()
    context = {
        "catalog_items": catalog_items,
    }
    return render(request, 'main/index.html', context)


def details(request, id):
    catalog_item = CatalogItem.objects.get(id=id)
    context = {
        'catalog_item': catalog_item
    }
    return render(request, 'main/details.html', context)


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            return render(request, 'main/signin.html', {"error": 'Invalid username or password. Try again.'})
    return render(request, 'main/signin.html')


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


def logout_user(request):
    logout(request)
    return redirect('main:home')

def add_review(request, id):
    if request.user.is_authenticated:
        catalog_item = CatalogItem.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                user_review = form.save(commit=False)
                user_review.user = request.user
                user_review.catalog_item = catalog_item
                user_review.comment = request.POST["comment"]
                user_review.rating = request.POST["rating"]
                user_review.save()
                return redirect("main:details", id)
        else:
            form = ReviewForm()
        return render(request, "main/details.html", {"form": form})
    else:
        return redirect("main:signin")

def user_reviews(request):
    # table
    return render(request, "main/userreviews.html")