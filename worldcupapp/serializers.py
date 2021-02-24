from rest_framework import serializers
from worldcupapp import models as worldcupapp_models


class WorldcupSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.Worldcup
        fields = "__all__"


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.BaseMedia
        fields = "__all__"


class TextMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.TextMedia
        fields = "__all__"


class ImageMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.ImageMedia
        fields = "__all__"


class GifMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.GifMedia
        fields = "__all__"


class VideoMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.VideoMedia
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = worldcupapp_models.Comment
        fields = "__all__"
