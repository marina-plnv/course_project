from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=200)
    release_date = models.DateField()
    average_rating = models.FloatField()

    def __str__(self):
        return self.name
