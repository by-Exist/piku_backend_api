from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField
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


class MediaListSerializer(serializers.HyperlinkedModelSerializer):

    url = NestedHyperlinkedIdentityField(
        view_name="media-detail",
        parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
    )

    class Meta:
        model = Media
        fields = [
            "id",
            "url",
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
