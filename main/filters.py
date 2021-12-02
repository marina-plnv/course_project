import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter

from .models import *


class ReviewFilter(django_filters.FilterSet):
    #start_date = DateFilter(field_name="date", lookup_expr='gte')
    #end_date = DateFilter(field_name="date", lookup_expr='lte')
    comment = CharFilter(field_name='comment', lookup_expr='icontains')

    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['user', 'date', 'likes']
