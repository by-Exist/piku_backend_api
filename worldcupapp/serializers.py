from django.urls import reverse
from rest_framework import serializers
from accountapp.serializers import UserListSerializer
from worldcupapp import models as worldcupapp_models
from worldcupapp import views as worldcupapp_views


# Worldcup Serializer
class WorldcupSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField("get_thumbnail")
    media_list_url = serializers.SerializerMethodField(
        method_name="get_media_list_url", read_only=True
    )
    comment_list_url = serializers.SerializerMethodField(
        method_name="get_comment_list_url", read_only=True
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
            "media_list_url",
            "comment_list_url",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "password": {"write_only": True},
        }

    def get_media_list_url(self, obj) -> str:
        request = self.context["view"].request
        url_ref = reverse("media-list", args=[obj.id])
        url_abs = request.build_absolute_uri(url_ref)
        return url_abs

    def get_comment_list_url(self, obj) -> str:
        request = self.context["view"].request
        url_ref = reverse("comment-list", args=[obj.id])
        url_abs = request.build_absolute_uri(url_ref)
        return url_abs

    def get_thumbnail(self, obj):
        media_model = worldcupapp_views.MediaViewSet.media_models[obj.media_type]
        thumbnail_media_qs = media_model.objects.filter(worldcup=obj).all()[:2]
        if obj.media_type in ("T", "V"):
            return [media.media for media in thumbnail_media_qs]
        else:
            request = self.context["request"]
            return [
                request.build_absolute_uri(media.media.url)
                for media in thumbnail_media_qs
            ]


class WorldcupListSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField("get_thumbnail")

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

    def get_thumbnail(self, obj):
        media_model = worldcupapp_views.MediaViewSet.media_models[obj.media_type]
        thumbnail_media_qs = media_model.objects.filter(worldcup=obj).all()[:2]
        if obj.media_type in ("T", "V"):
            return [media.media for media in thumbnail_media_qs]
        else:
            request = self.context["request"]
            return [
                request.build_absolute_uri(media.media.url)
                for media in thumbnail_media_qs
            ]

    def create(self, validated_data):
        validated_data |= {"creator": self.context["view"].request.user}
        return super().create(validated_data)


# Media Serializer
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.BaseMedia
        fields = (
            "id",
            "title",
            "media",
            "win_count",
            "choice_count",
        )


class MediaListSerializer(MediaSerializer):

    url = serializers.SerializerMethodField(method_name="get_media_url")

    class Meta:
        model = worldcupapp_models.BaseMedia
        fields = (
            "id",
            "url",
            "title",
            "media",
            "win_count",
            "choice_count",
        )

    def get_media_url(self, obj) -> str:
        request = self.context["request"]
        rel_url = reverse("media-detail", args=(obj.worldcup.pk, obj.pk))
        return request.build_absolute_uri(rel_url)

    def create(self, validated_data):
        worldcup_pk = self.context["view"].kwargs["worldcup_pk"]
        worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
        validated_data |= {"worldcup": worldcup}
        return super().create(validated_data)


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
class CommentSerializer(serializers.HyperlinkedModelSerializer):

    media = serializers.SerializerMethodField(method_name="get_media_url")

    class Meta:
        model = worldcupapp_models.Comment
        fields = (
            "id",
            "comment",
            "writer",
            "worldcup",
            "media",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "writer": {"read_only": True},
            "worldcup": {"read_only": True},
        }

    def get_media_url(self, obj) -> str:
        if obj.media == None:
            return None
        rel_url = reverse(viewname="media-detail", args=(obj.worldcup.pk, obj.media.pk))
        request = self.context["request"]
        return request.build_absolute_uri(rel_url)


class CommentListSerializer(serializers.HyperlinkedModelSerializer):

    media_id = serializers.IntegerField(write_only=True, allow_null=True)
    url = serializers.SerializerMethodField(method_name="get_url")
    media = serializers.SerializerMethodField(method_name="get_media_url")

    class Meta:
        model = worldcupapp_models.Comment
        fields = (
            "id",
            "url",
            "comment",
            "writer",
            "worldcup",
            "media",
            "media_id",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "writer": {"read_only": True},
            "worldcup": {"read_only": True},
        }

    def get_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.get_absolute_url())

    def get_media_url(self, obj) -> str:
        if obj.media == None:
            return None
        return self.context["request"].build_absolute_uri(obj.media.get_absolute_url())

    def create(self, validated_data):
        user = self.context["request"].user
        worldcup = worldcupapp_models.Worldcup.objects.get(
            pk=self.context["view"].kwargs["worldcup_pk"]
        )
        validated_data |= {"writer": user, "worldcup": worldcup}
        media_id = validated_data.pop("media_id")
        if media_id:
            media = worldcupapp_models.BaseMedia.objects.get(pk=media_id)
            validated_data |= {"media": media}
        return super().create(validated_data)
