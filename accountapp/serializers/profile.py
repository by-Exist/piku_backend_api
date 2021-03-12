from rest_framework import serializers
from accountapp.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "avatar", "email")
        extra_kwargs = {"email": {"read_only": True}}


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ("url", "nickname", "avatar", "email")
