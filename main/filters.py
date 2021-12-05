import django_filters
from django_filters import CharFilter

from .models import *


class ReviewFilter(django_filters.FilterSet):
    comment = CharFilter(field_name='comment', lookup_expr='icontains')

    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['user', 'date', 'likes', 'average_star_rating']
