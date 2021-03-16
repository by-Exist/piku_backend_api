from django.db import models
from rest_framework import serializers
from accountapp.serializers import UserListSerializer
from ..models import Worldcup


# class InnerThumbnailListSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         iterable = data.all()[:2] if isinstance(data, models.Manager) else data
#         return [self.child.to_representation(item) for item in iterable]


# # TODO: 미디어를 작업한 다음에 해야겠구만.
# class InnerMediaBodyField(serializers.CharField):
#     def to_representation(self, value):
#         if value.worldcup.media_type in ["Image", "Gif"]:
#             return value.body.url
#         else:
#             return value.body


class WorldcupDetailSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    # thumbnail = InnerThumbnailListSerializer(
    #     read_only=True, child=InnerMediaBodyField(), source="media_set"
    # )

    class Meta:
        model = Worldcup
        fields = (
            "id",
            # "thumbnail",
            "title",
            "subtitle",
            "media_type",
            "publish_type",
            "password",
            "play_count",
            "created_at",
            "updated_at",
            "creator",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "password": {"write_only": True},
        }


class WorldcupListSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    # thumbnail = InnerThumbnailListSerializer(
    #     read_only=True, child=InnerMediaBodyField(), source="media_set"
    # )

    class Meta:
        model = Worldcup
        fields = (
            "id",
            "url",
            # "thumbnail",
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
