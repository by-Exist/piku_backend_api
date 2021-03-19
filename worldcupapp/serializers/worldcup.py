from django.db import models
from rest_framework import serializers
from accountapp.serializers import UserListSerializer
from ..models import Worldcup


class ThumbnailListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all()[:2] if isinstance(data, models.Manager) else []
        return [self.child.to_representation(item) for item in iterable]


class ThumbnailListSerializerCharField(serializers.CharField):
    def to_representation(self, value):
        body = value.body
        if hasattr(body, "url"):
            url = self.context["request"].build_absolute_uri(body.url)
            return url
        else:
            return body


class WorldcupDetailSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    thumbnail = ThumbnailListSerializer(
        read_only=True,
        source="media_set",
        child=ThumbnailListSerializerCharField(),
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
            "view_count",
            "play_count",
            "created_at",
            "updated_at",
            "creator",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate_publish_type(self, publish_type):
        if publish_type in (
            Worldcup.PublishType.PUBLIC.value,
            Worldcup.PublishType.PASSWORD.value,
        ):
            if not self.context["view"].get_object().media_set.count() >= 2:
                return publish_type
            raise serializers.ValidationError("최소 2개 이상의 media를 업로드 해 주세요.")
        return publish_type


class WorldcupListSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    thumbnail = ThumbnailListSerializer(
        read_only=True,
        source="media_set",
        child=ThumbnailListSerializerCharField(),
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


class NoBodyPostSerializer(serializers.Serializer):

    pass
