from collections.abc import Mapping
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from ..models import Media, TextMedia, ImageMedia, GifMedia, VideoMedia


class MediaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "title",
            "win_count",
            "view_count",
            "choice_count",
            "body",
        ]


class MediaListSerializer(serializers.ModelSerializer):

    # TODO: Nested URL 구현

    class Meta:
        model = Media
        fields = [
            "id",
            # "url",
            "title",
            "body",
        ]

    def create(self, validated_data):
        worldcup = self.context["view"].parent_object
        validated_data |= {"worldcup": worldcup}
        return super().create(validated_data)


class TextMediaDetailSerializer(serializers.ModelSerializer):
    class Meta(MediaDetailSerializer.Meta):
        model = TextMedia


class TextMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = TextMedia


class ImageMediaDetailSerializer(serializers.ModelSerializer):
    class Meta(MediaDetailSerializer.Meta):
        model = ImageMedia


class ImageMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = ImageMedia


class GifMediaDetailSerializer(serializers.ModelSerializer):
    class Meta(MediaDetailSerializer.Meta):
        model = GifMedia


class GifMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = GifMedia


class VideoMediaDetailSerializer(serializers.ModelSerializer):
    class Meta(MediaDetailSerializer.Meta):
        model = VideoMedia


class VideoMediaListSerializer(MediaListSerializer):
    class Meta(MediaListSerializer.Meta):
        model = VideoMedia


class MediaDetailPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        TextMedia: TextMediaDetailSerializer,
        ImageMedia: ImageMediaDetailSerializer,
        GifMedia: GifMediaDetailSerializer,
        VideoMedia: VideoMediaDetailSerializer,
    }


class MediaListPolymorphicSerializer(PolymorphicSerializer):

    # _get_resource_type_from_mapping 참고
    resource_type_mapping = {
        "Text": "TextMedia",
        "Image": "ImageMedia",
        "Gif": "GifMedia",
        "Video": "VideoMedia",
    }

    model_serializer_mapping = {
        TextMedia: TextMediaListSerializer,
        ImageMedia: ImageMediaListSerializer,
        GifMedia: GifMediaListSerializer,
        VideoMedia: VideoMediaListSerializer,
    }

    # resourcetype 필드 제거
    def to_representation(self, instance):
        if isinstance(instance, Mapping):
            resource_type = self._get_resource_type_from_mapping(instance)
            serializer = self._get_serializer_from_resource_type(resource_type)
        else:
            resource_type = self.to_resource_type(instance)
            serializer = self._get_serializer_from_model_or_instance(instance)
        ret = serializer.to_representation(instance)
        return ret

    # resourcetype 필드 제거
    def to_internal_value(self, data):
        resource_type = self._get_resource_type_from_mapping(data)
        serializer = self._get_serializer_from_resource_type(resource_type)
        ret = serializer.to_internal_value(data)
        return ret

    # request의 body에서 추출하던 resource_type을 worldcup의 media_type에서 가져오도록 수정
    def _get_resource_type_from_mapping(self, mapping):
        return self.resource_type_mapping[self.context["view"].parent_object.media_type]
