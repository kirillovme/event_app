from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Coordinate(models.Model):
    """Модель координат."""

    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"


class Event(models.Model):
    """Модель события."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    coordinate = models.ForeignKey(Coordinate, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return date.today() > self.end_date


class Weather(models.Model):
    """Модель прогноза погоды."""

    coordinate = models.ForeignKey(Coordinate, on_delete=models.CASCADE)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Weather in {self.coordinate}"
