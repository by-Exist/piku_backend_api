from django.contrib.auth import get_user_model
from rest_framework import serializers
from accountapp import models as accountapp_models
from backend.mixins import ActionSerializerMixin


class ProfileSerializer(ActionSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = accountapp_models.Profile
        fields = "__all__"


class UserSerializer(ActionSerializerMixin, serializers.ModelSerializer):

    avatar = serializers.ImageField(source="profile.avatar")
    nickname = serializers.CharField(source="profile.nickname")

    class Meta:
        model = accountapp_models.CustomUser
        fields = "__all__"
        # TODO: write_only field가 swagger에 정상적으로 표기되지 않는 문제 확인
        # https://www.google.com/search?q=write_only+field+swagger&oq=write_only+field+swagger&aqs=chrome..69i57.5132j0j7&sourceid=chrome&ie=UTF-8
        extra_kwargs = {"password": {"write_only": True}}
        action_fields = {
            "list": {
                "fields": ["id", "username", "nickname", "avatar"],
            },
            # TODO: ...
            # "create": {
            #     "fields": ["username", "password"],
            # },
            # "retrieve": {
            #     "fields": ["username", "password"],
            # },
            # "update": {
            #     "fields": ["password"],
            # },
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    # TODO: ...
    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)
