from django.db import models
from users.models import User


# Create your models here.
class Route(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    reward = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Waypoint(models.Model):
    route = models.ForeignKey(Route, related_name="waypoints", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Waypoint {self.order} for {self.route.name}"


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "route")

    def __str__(self):
        return f"User {self.user_id} - Route {self.route.name} - Completed: {self.completed}"
