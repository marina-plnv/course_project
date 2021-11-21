from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# from taggit.managers import TaggableManager

class CatalogItem(models.Model):
    GROUP_CHOICES = [
        ("movie", "Movie"),
        ("book", "Book")
    ]
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=15, choices=GROUP_CHOICES)
    image = models.URLField(default=None, null=True)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    catalog_item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # tags = TaggableManager()
    comment = models.TextField(max_length=2000)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
