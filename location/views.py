from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Route, Waypoint, UserRoute, Event
from .serializers import (
    RouteSerializer,
    WaypointSerializer,
    UserRouteSerializer,
    EventSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]


class WaypointViewSet(viewsets.ModelViewSet):
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer
    permission_classes = [IsAdminUser]


class UserRouteViewSet(viewsets.ModelViewSet):
    serializer_class = UserRouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserRoute.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def demo_mission(self, request):
        profile = request.user.profile
        old_level = profile.level
        profile.add_experience(120)
        level_up = profile.level > old_level
        return Response(
            {
                "status": "Mission completed",
                "level_up": level_up,
                "new_level": profile.level,
                "experience": profile.experience,
            }
        )

    @action(detail=True, methods=["post"])
    def complete_route(self, request, pk=None):
        route = self.get_object().route
        user = request.user
        profile = user.profile
        if not UserRoute.objects.filter(
            user=user, route=route, completed=True
        ).exists():
            profile.add_experience(route.reward or 0)
            UserRoute.objects.filter(user=user, route=route).update(completed=True)
            return Response({"status": "Route completed"})

        return Response(
            {"status": "Route already completed or user-route not found"}, status=400
        )


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
