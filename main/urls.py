from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.index, name="home"),
    path('details/<int:id>/', views.details, name="details"),
    path('sign-in/', views.signin, name="signin"),
    path('sign-up/', views.signup, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('user-reviews/', views.user_reviews, name="userreviews"),
    path('add-review/<int:id>/', views.add_review, name="addreview"),
    path('like-review/<int:review_id>/', views.like_review, name="likereview"),
    path('review-details/<int:id>/', views.review_details, name="reviewdetails"), #???????????????????????????
    path('add-rating/<int:review_id>/', views.add_star_rating, name="addrating"),#????????????????????????????????
    #path('star-rating/<int:item_id>/<int:review_id>/', views.star_rating, name="starrating"),
    path('movies/', views.movies, name="movies"),
    path('books/', views.books, name="books"),
    path('edit-review/<int:id>/', views.edit_review, name="editreview"),
    path('delete-review/<int:id>/', views.delete_review, name="deletereview"),

]
