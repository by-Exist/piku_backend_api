from rest_framework import serializers
from django.contrib.auth import get_user_model
from accountapp import models as accountapp_models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountapp_models.Profile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountapp_models.CustomUser
        fields = "__all__"
