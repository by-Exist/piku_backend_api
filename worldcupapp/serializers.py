from django.urls import reverse
from rest_framework import serializers
from worldcupapp import models as worldcupapp_models


# Worldcup Serializer
class WorldcupSerializer(serializers.ModelSerializer):

    media_list = serializers.SerializerMethodField(
        method_name="get_media_list_url", read_only=True
    )

    class Meta:
        model = worldcupapp_models.Worldcup
        fields = (
            "title",
            "subtitle",
            "media_type",
            "media_list",
            "publish_type",
            "password",
            "play_count",
            "creator",
        )
        extra_kwargs = {
            "media_type": {"read_only": True},
            "creator": {"read_only": True},
            "password": {"write_only": True},
        }

    def get_media_list_url(self, obj):
        request = self.context["view"].request
        url_ref = reverse("media-list", args=[obj.id])
        url_abs = request.build_absolute_uri(url_ref)
        return url_abs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class WorldcupListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = worldcupapp_models.Worldcup
        fields = (
            "id",
            "url",
            "title",
            "subtitle",
            "media_type",
            "publish_type",
            # "password",
            "play_count",
            "creator",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "password": {"write_only": True},
            "publish_type": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data |= {"creator": self.context["view"].request.user}
        return super().create(validated_data)


# Media Serializer
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = (
            "id",
            "title",
            "win_count",
            "choice_count",
            "media",
        )


class MediaListSerializer(MediaSerializer):

    url = serializers.SerializerMethodField(method_name="get_media_url")

    class Meta:
        model = None
        fields = (
            "id",
            "url",
            "title",
            "win_count",
            "choice_count",
            "media",
        )

    def create(self, validated_data):
        worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
        worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
        validated_data |= {"worldcup": worldcup}
        return super().create(validated_data)

    def get_media_url(self, obj):
        request = self.context["request"]
        rel_url = reverse("media-detail", args=(obj.worldcup.pk, obj.pk))
        return request.build_absolute_uri(rel_url)


class TextMediaSerializer(MediaSerializer):
    class Meta(MediaSerializer.Meta):
        model = worldcupapp_models.TextMedia


class TextMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = worldcupapp_models.TextMedia


class ImageMediaSerializer(MediaSerializer):
    class Meta(MediaSerializer.Meta):
        model = worldcupapp_models.ImageMedia


class ImageMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = worldcupapp_models.ImageMedia


class GifMediaSerializer(MediaSerializer):
    class Meta(MediaSerializer.Meta):
        model = worldcupapp_models.GifMedia


class GifMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = worldcupapp_models.GifMedia


class VideoMediaSerializer(MediaSerializer):
    class Meta(MediaSerializer.Meta):
        model = worldcupapp_models.VideoMedia


class VideoMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = worldcupapp_models.VideoMedia


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.Comment
        fields = "__all__"
