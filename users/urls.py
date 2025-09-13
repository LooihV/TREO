from django.urls import path, include

from rest_framework import routers

from . import views

routers = routers.DefaultRouter()

routers.register(r"users", views.UserViewSet)
routers.register(r"achievements", views.AchievementViewSet)
routers.register(
    r"user-achievements", views.UserAchievementViewSet, basename="user-achievements"
)
routers.register(r"profiles", views.ProfileViewSet, basename="profiles")
routers.register(r"user-details", views.UserDetailViewSet, basename="user-details")
routers.register(
    r"public-profiles", views.PublicProfileViewSet, basename="public-profiles"
)


urlpatterns = [
    path("", include(routers.urls)),
    path("me/", views.MeView.as_view(), name="me"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
