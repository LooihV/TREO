from rest_framework import viewsets, generics
from .models import User, UserAchievement, Achievement, Profile
from .serializers import (
    UserSerializer,
    UserAchievementSerializer,
    UserDetailSerializer,
    AchievementSerializer,
    ProfileSerializer,
    PublicProfileSerializer,
    RegisterSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


# Create your views here.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserAchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


class PublicProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = "user__username"

    def get_queryset(self):
        queryset = Profile.objects.all()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.exclude(user=user)
        return queryset


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
