from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .filters import ReviewFilter


### calculate average rating

def index(request):
    latest_reviews = Review.objects.all().order_by('-pk', '-date')
    highly_rated_reviews = Review.objects.all().order_by('-rating', '-date')
    context = {
        "latest_reviews": latest_reviews[:6],
        "highly_rated_reviews": highly_rated_reviews[:6],
    }
    return render(request, 'main/index.html', context)


def movies(request): ###### display high average rate movies
    movies = CatalogItem.objects.all().filter(group='movie')
    for movie in movies:
        movie_latest_review = Review.objects.all().filter(catalog_item=movie).order_by('-date')[0]
        movie.review = movie_latest_review.comment
        movie.review_date = movie_latest_review.date
        movie.review_user = movie_latest_review.user
    context = {
        "movies": movies,
    }
    return render(request, 'main/movies.html', context)


def details(request, id):
    catalog_item = CatalogItem.objects.get(id=id)
    reviews = Review.objects.all().filter(catalog_item=catalog_item).order_by('-date')
    context = {
        'catalog_item': catalog_item,
        'reviews': reviews
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


def review(request, id):
    catalog_item = CatalogItem.objects.get(id=id)
    context = {
        'catalog_item': catalog_item,
    }
    return render(request, 'main/addreview.html', context)


def add_review(request, id):
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


def user_reviews(request):
    # user???????
    reviews=Review.objects.all().filter(user=request.user).order_by('-date')
    review_filter=ReviewFilter(request.GET, queryset=reviews)
    reviews=review_filter.qs
    context={
        "reviews": reviews,
        "review_filter": review_filter,
    }
    return render(request, "main/userreviews.html", context)
