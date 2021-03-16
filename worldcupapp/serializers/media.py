from django.db import models
from rest_framework import serializers
from accountapp.serializers import UserListSerializer

# from rest_framework_nested.relations import NestedHyperlinkedRelatedField


# # Media Serializer
# class BodyField(serializers.CharField):
#     def to_representation(self, value):
#         worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
#         media_type = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk).media_type
#         if media_type in ("Image", "Gif"):
#             return self.context["request"].build_absolute_uri(value)
#         return value


# class MediaSerializer(serializers.ModelSerializer):

#     body = BodyField()

#     class Meta:
#         model = worldcupapp_models.BaseMedia
#         fields = (
#             "id",
#             "title",
#             "body",
#             "win_count",
#             "choice_count",
#         )


# class MediaListSerializer(MediaSerializer):

#     url = NestedHyperlinkedRelatedField(
#         read_only=True,
#         view_name="media-detail",
#         parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
#     )
#     body = BodyField()

#     class Meta:
#         model = worldcupapp_models.BaseMedia
#         fields = (
#             "id",
#             "url",
#             "title",
#             "body",
#         )

#     def create(self, validated_data):
#         worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
#         worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
#         validated_data |= {"worldcup": worldcup}
#         return super().create(validated_data)


# class TextMediaSerializer(MediaSerializer):
#     class Meta(MediaSerializer.Meta):
#         model = worldcupapp_models.TextMedia


# class TextMediaListSerializer(MediaListSerializer):
#     class Meta(MediaListSerializer.Meta):
#         model = worldcupapp_models.TextMedia


# class ImageMediaSerializer(MediaSerializer):
#     class Meta(MediaSerializer.Meta):
#         model = worldcupapp_models.ImageMedia


# class ImageMediaListSerializer(MediaListSerializer):
#     class Meta(MediaListSerializer.Meta):
#         model = worldcupapp_models.ImageMedia


# class GifMediaSerializer(MediaSerializer):
#     class Meta(MediaSerializer.Meta):
#         model = worldcupapp_models.GifMedia


# class GifMediaListSerializer(MediaListSerializer):
#     class Meta(MediaListSerializer.Meta):
#         model = worldcupapp_models.GifMedia


# class VideoMediaSerializer(MediaSerializer):
#     class Meta(MediaSerializer.Meta):
#         model = worldcupapp_models.VideoMedia


# class VideoMediaListSerializer(MediaListSerializer):
#     class Meta(MediaListSerializer.Meta):
#         model = worldcupapp_models.VideoMedia
