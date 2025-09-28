from django.db import models


class Trip(models.Model):
    name = models.CharField(max_length=200, blank=True)
    current_location = models.CharField(max_length=300)
    pickup = models.CharField(max_length=300)
    dropoff = models.CharField(max_length=300)
    current_cycle_hours = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Trip {self.id} - {self.name or self.pickup}->{self.dropoff}"


class Waypoint(models.Model):
    trip = models.ForeignKey(Trip, related_name='waypoints', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    order = models.IntegerField(default=0)


    class Meta:
        ordering = ['order']    