from django.contrib import admin
from django.contrib.admin import display

from .models import *

admin.site.register(CatalogItem)
#admin.site.register(Review)
admin.site.register(RatingStar)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "star", "get_review_name")

    @display(ordering='review__review_title', description='review_title')
    def get_review_name(self, obj):
        return obj.review.review_title

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "review_title", "catalog_item", "rating","total_likes", "average_star_rating")

