from django.contrib.auth import get_user_model
from rest_framework import serializers
from accountapp import models as accountapp_models

# ProfileSerializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountapp_models.Profile
        fields = ("nickname", "avatar", "email")


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = accountapp_models.Profile
        fields = ("url", "nickname", "avatar", "email")


# UserSerializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileListSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
            "profile",
            "is_active",
            "last_login",
            "date_joined",
        )
        extra_kwargs = {
            "username": {"read_only": True},
            "password": {"write_only": True},
            "last_login": {"read_only": True},
            "date_joined": {"read_only": True},
        }

    def update(self, instance, validated_data):
        pw = validated_data.pop("password")
        instance.set_password(pw)
        instance.save()
        return instance


class UserListSerializer(serializers.HyperlinkedModelSerializer):

    profile = ProfileListSerializer(read_only=True)
    nickname = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "url",
            "username",
            "profile",
            "password",
            "nickname",
            "email",
        )
        extra_kwargs = {
            "url": {"view_name": "account-detail"},
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "date_joined": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):
        email = validated_data.pop("email")
        nickname = validated_data.pop("nickname")
        user = get_user_model().objects.create_user(**validated_data, is_active=False)
        accountapp_models.Profile.objects.create(
            user=user, nickname=nickname, email=email
        )
        return user


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    new_password = serializers.CharField()
    repeat_new_password = serializers.CharField()


# Token Serializer
# https://github.com/axnsan12/drf-yasg/issues/407
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
