from rest_framework import serializers
from accountapp import models as accountapp_models

# ProfileSerializer
class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.HyperlinkedRelatedField(
        view_name="customuser-detail", read_only=True
    )

    class Meta:
        model = accountapp_models.Profile
        fields = ("id", "nickname", "avatar", "email", "user")


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = accountapp_models.Profile
        fields = ("id", "url", "nickname", "avatar", "email", "user")
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data |= {"user": self.context["view"].request.user}
        return super().create(validated_data)


# UserSerializer
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileListSerializer(read_only=True)

    class Meta:
        model = accountapp_models.CustomUser
        fields = ("id", "username", "password", "profile", "last_login", "date_joined")
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

    profile = serializers.HyperlinkedRelatedField(
        view_name="profile-detail", read_only=True
    )

    class Meta:
        model = accountapp_models.CustomUser
        fields = ("id", "url", "profile", "username", "password", "date_joined")
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


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
