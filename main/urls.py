from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name="home"),
    path('details/<int:id>/', views.details, name="details"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('user-reviews/', views.user_reviews, name="userreviews")
]