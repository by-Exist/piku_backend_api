from django.db import models
from rest_framework import serializers
from accountapp.serializers import UserListSerializer
from worldcupapp import models as worldcupapp_models

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


# # Comment Serializer
# class AuthenticatedUserCommentPasswordSerializer(serializers.Serializer):

#     pass


# class AnonymousUserCommentPasswordSerializer(serializers.Serializer):

#     password = serializers.CharField(
#         style={"input_type": "password", "placeholder": "Password"},
#     )


# class CommentSerializer(serializers.HyperlinkedModelSerializer):

#     writer = UserListSerializer(read_only=True)
#     media = MediaListSerializer(read_only=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "id",
#             "comment",
#             "writer",
#             "media",
#             "created_at",
#             "updated_at",
#         )
#         extra_kwargs = {
#             "writer": {"read_only": True},
#             "worldcup": {"read_only": True},
#         }


# class CommentListSerializer(serializers.HyperlinkedModelSerializer):

#     url = NestedHyperlinkedRelatedField(
#         read_only=True,
#         view_name="media-detail",
#         parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
#     )
#     writer = UserListSerializer(read_only=True)
#     media = MediaListSerializer(read_only=True)
#     media_id = serializers.IntegerField(write_only=True, allow_null=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "id",
#             "url",
#             "writer",
#             "anonymous_nickname",
#             "comment",
#             "worldcup",
#             "media",
#             "media_id",
#             "created_at",
#             "updated_at",
#         )
#         extra_kwargs = {
#             "writer": {"read_only": True},
#             "worldcup": {"read_only": True},
#             "anonymous_nickname": {"read_only": True},
#         }

#     def create(self, validated_data):
#         user = self.context["request"].user
#         worldcup = worldcupapp_models.Worldcup.objects.get(
#             pk=self.context["view"].kwargs["worldcup_pk"]
#         )
#         validated_data |= {
#             "writer": user,
#             "worldcup": worldcup,
#             "anonymous_nickname": "",
#         }
#         media_id = validated_data.get("media_id")
#         if media_id:
#             media = worldcupapp_models.BaseMedia.objects.get(pk=media_id)
#             validated_data |= {"media": media}
#         return super().create(validated_data)


# class AnonymouseCommentUpdateSerializer(serializers.ModelSerializer):

#     check_password = serializers.CharField(
#         write_only=True,
#         style={"input_type": "password", "placeholder": "Password"},
#     )
#     media_id = serializers.IntegerField(write_only=True, allow_null=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "check_password",
#             "comment",
#             "media_id",
#         )

#     def update(self, instance, validated_data):
#         if "check_password" in validated_data:
#             validated_data.pop("check_password")
#         return super().update(instance, validated_data)


# class AnonymouseCommentCreateSerializer(serializers.ModelSerializer):

#     media_id = serializers.IntegerField(write_only=True, allow_null=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "anonymous_nickname",
#             "anonymous_password",
#             "comment",
#             "media_id",
#         )
#         extra_kwargs = {
#             "anonymous_password": {
#                 "write_only": True,
#                 "style": {"input_type": "password", "placeholder": "Password"},
#             },
#         }

#     def create(self, validated_data):
#         worldcup = worldcupapp_models.Worldcup.objects.get(
#             pk=self.context["view"].kwargs["worldcup_pk"]
#         )
#         validated_data |= {"writer": None, "worldcup": worldcup}
#         media_id = validated_data.get("media_id", None)
#         if media_id:
#             media = worldcupapp_models.BaseMedia.objects.get(pk=media_id)
#             validated_data |= {"media": media}
#         return super().create(validated_data)


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
        model = worldcupapp_models.Worldcup
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
        model = worldcupapp_models.Worldcup
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
