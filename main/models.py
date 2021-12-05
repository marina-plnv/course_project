from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
#from taggit.managers import TaggableManager


class CatalogItem(models.Model):
    GROUP_CHOICES = [
        ("movie", "Movie"),
        ("book", "Book")
    ]
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=15, choices=GROUP_CHOICES)
    image = models.ImageField(upload_to='img/', default=None)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    review_title = models.CharField(max_length=100, default="My review")
    catalog_item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_user")
    #tags = TaggableManager()
    comment = RichTextUploadingField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="review_like")
    average_star_rating = models.FloatField(default=0)

    def total_likes(self):
        return (self.likes.count() if self.likes else 0)

    def __str__(self):
        return self.user.username


class RatingStar(models.Model):
    value = models.SmallIntegerField("value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating_user")
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="star")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="rating_review", verbose_name="review")

    def __str__(self):
        return f"{self.star}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
