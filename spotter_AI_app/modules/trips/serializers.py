from rest_framework import serializers

from spotter_AI_app.models.trip_model import Trip, Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    waypoints = WaypointSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ['id','name','current_location','pickup','dropoff','current_cycle_hours','created_at','waypoints']
