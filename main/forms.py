from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("review_title", "comment", "rating")
