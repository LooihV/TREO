from .models import User, Profile, Achievement, UserAchievement
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "is_staff", "date_joined"]
        read_only_fields = ["id", "is_active", "is_staff", "date_joined"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "photo", "level", "experience", "bio"]
        read_only_fields = ["id", "user"]


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "name", "description", "icon"]
        read_only_fields = ["id"]


class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ["id", "user", "achievement", "date_earned"]
        read_only_fields = ["id", "user", "date_earned"]


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    achievements = UserAchievementSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
            "profile",
            "achievements",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "is_staff",
            "date_joined",
            "profile",
            "achievements",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "address",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data.get("phone", ""),
            address=validated_data.get("address", ""),
        )
        Profile.objects.create(user=user)
        return user


class PublicProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "photo", "level", "experience", "bio"]
        read_only_fields = ["user"]
