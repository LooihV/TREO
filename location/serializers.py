from .models import Route, Waypoint, UserRoute
from rest_framework import serializers


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = ["id", "route", "name", "latitude", "longitude", "order"]
        read_only_fields = ["id"]


class RouteSerializer(serializers.ModelSerializer):
    waypoints = WaypointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ["id", "name", "type", "icon", "color", "reward", "waypoints"]
        read_only_fields = ["id", "waypoints"]


class UserRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoute
        fields = ["id", "user", "route", "completed"]
        read_only_fields = ["id", "user"]
