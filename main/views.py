from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import ReviewFilter
from django.db.models import Avg


def index(request):
    latest_reviews = Review.objects.all().order_by('-date', '-pk')
    highly_rated_reviews = Review.objects.all().order_by('-rating', '-date')
    context = {
        "latest_reviews": latest_reviews[:6],
        "highly_rated_reviews": highly_rated_reviews[:6],
    }
    return render(request, 'main/index.html', context)


def movies(request):
    movies = CatalogItem.objects.all().filter(group='movie')
    context = {
        "movies": movies,
    }
    return render(request, 'main/movies.html', context)


def books(request):
    books = CatalogItem.objects.all().filter(group='book')
    context = {
        "books": books,
    }
    return render(request, 'main/books.html', context)


def details(request, id):
    catalog_item = CatalogItem.objects.get(id=id)
    reviews = Review.objects.all().filter(catalog_item=catalog_item).order_by('-date')
    context = {
        'catalog_item': catalog_item,
        'reviews': reviews,
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


def update_average_rating(catalog_item):
    reviews = Review.objects.all().filter(catalog_item=catalog_item)
    avg_rate = reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rate is not None:
        avg_rate = round(avg_rate, 2)
        CatalogItem.objects.filter(id=catalog_item.id).update(average_rating=avg_rate)


def add_review(request, id):
    if request.user.is_authenticated:
        catalog_item = CatalogItem.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                user_review = form.save(commit=False)
                user_review.user = request.user
                user_review.catalog_item = catalog_item
                user_review.review_title = request.POST["review_title"]
                user_review.comment = request.POST["comment"]
                user_review.rating = request.POST["rating"]
                user_review.save()
                update_average_rating(catalog_item)
                return redirect("main:details", id)
        else:
            form = ReviewForm()
        return render(request, 'main/addreview.html', {'form': form, 'catalog_item': catalog_item})
    return redirect('main:details', id)


def like_review(request, review_id):
    if request.user.is_authenticated:
        review = Review.objects.get(id=review_id)
        if review.user != request.user:
            if request.method == "POST":
                review.likes.add(request.user)
        return redirect('main:reviewdetails', review_id)
    return redirect('main:signin')


def user_reviews(request):
    if request.user.is_authenticated:
        reviews = Review.objects.all().filter(user=request.user).order_by('-date')
        filter = ReviewFilter(request.GET, queryset=reviews)
        reviews = filter.qs
        context = {
            "reviews": reviews,
            "filter": filter,
        }
        return render(request, "main/userreviews.html", context)
    return redirect('main:home')


def edit_review(request, id):
    review = get_object_or_404(Review, id=id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ReviewForm(request.POST or None, instance=review)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                update_average_rating(review.catalog_item)
                return redirect("main:userreviews")
        else:
            form = ReviewForm(instance=review)
        return render(request, 'main/editreview.html', {"form": form})
    return redirect('main:signin')


def delete_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    update_average_rating(review.catalog_item)
    return redirect('main:userreviews')


def update_average_review_star_rating(review_id):
    review_ratings = Rating.objects.all().filter(review=Review.objects.get(id=review_id))
    avg_star_rating = review_ratings.aggregate(Avg('star'))['star__avg']
    if avg_star_rating is not None:
        avg_star_rating = round(avg_star_rating, 2)
        Review.objects.filter(id=review_id).update(average_star_rating=avg_star_rating)


def add_star_rating(request, review_id):
    review=Review.objects.get(id=review_id)
    if review.user != request.user:
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=request.user,
                review_id=int(review_id),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            update_average_review_star_rating(review_id)
            redirect('main:reviewdetails', review_id)
    return HttpResponse(status=400)


def review_details(request, id):
    review = Review.objects.get(id=id)
    star_form = RatingForm()
    context = {
        'review': review,
        'star_form': star_form,
    }
    return render(request, "main/reviewdetails.html", context)

