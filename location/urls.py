from django.urls import path, include

from rest_framework import routers

from . import views

routers = routers.DefaultRouter()
routers.register(r"routes", views.RouteViewSet)
routers.register(r"waypoints", views.WaypointViewSet)
routers.register(r"user-routes", views.UserRouteViewSet, basename="user-routes")
routers.register(r"events", views.EventViewSet)


urlpatterns = [
    path("", include(routers.urls)),
]
