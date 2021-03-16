from django.db import models
from rest_framework import serializers
from accountapp.serializers import UserListSerializer
from ..models import Worldcup


# Worldcup Serializer
class ThumbnailListSerializer(serializers.ListSerializer):
    """두 개의 미디어만 추출하도록 제한"""

    def to_representation(self, data):
        iterable = data.all()[:2] if isinstance(data, models.Manager) else data
        return [self.child.to_representation(item) for item in iterable]


class MediaBodyField(serializers.CharField):
    def to_representation(self, value):
        if value.worldcup.media_type in ["I", "G"]:
            return value.body.url
        else:
            return value.body


class WorldcupSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    thumbnail = ThumbnailListSerializer(
        read_only=True, child=MediaBodyField(), source="media_set"
    )
    media_list = serializers.HyperlinkedIdentityField(
        view_name="media-list", lookup_url_kwarg="worldcup_pk"
    )
    comment_list = serializers.HyperlinkedIdentityField(
        view_name="comment-list", lookup_url_kwarg="worldcup_pk"
    )

    class Meta:
        model = Worldcup
        fields = (
            "id",
            "thumbnail",
            "title",
            "subtitle",
            "media_type",
            "publish_type",
            "password",
            "play_count",
            "created_at",
            "updated_at",
            "creator",
            "media_list",
            "comment_list",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "password": {"write_only": True},
        }


class WorldcupListSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    thumbnail = ThumbnailListSerializer(
        read_only=True, child=MediaBodyField(), source="media_set"
    )

    class Meta:
        model = Worldcup
        fields = (
            "id",
            "url",
            "thumbnail",
            "title",
            "subtitle",
            "media_type",
            "publish_type",
            "creator",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "media_type": {"required": True},
            "publish_type": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data |= {"creator": self.context["view"].request.user}
        return super().create(validated_data)
