from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name="home"),
    path('details/<int:id>/', views.details, name="details"),
    path('sign-in/', views.signin, name="signin"),
    path('sign-up/', views.signup, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('review/<int:id>', views.review, name="review"),
    path('user-reviews/', views.user_reviews, name="userreviews"),
    path('add-review/<int:id>/', views.add_review, name="addreview"),
]
