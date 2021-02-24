from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from worldcupapp import models as worldcupapp_models
from worldcupapp import serializers as worldcupapp_serializer


class WorldcupViewSet(viewsets.ModelViewSet):
    queryset = worldcupapp_models.Worldcup.objects.all()
    serializer_class = worldcupapp_serializer.WorldcupSerializer


class MediaViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        try:
            worldcup = get_object_or_404(
                worldcupapp_models.Worldcup, pk=self.kwargs["worldcup_pk"]
            )
        except KeyError:
            return worldcupapp_models.BaseMedia
        media_models = {
            "T": worldcupapp_models.TextMedia,
            "I": worldcupapp_models.ImageMedia,
            "G": worldcupapp_models.GifMedia,
            "V": worldcupapp_models.VideoMedia,
        }
        MediaModel = media_models[worldcup.media_type]
        return MediaModel.objects.all()

    def get_serializer_class(self):
        try:
            worldcup = worldcupapp_models.Worldcup.objects.get(
                self.kwargs["worldcup_pk"]
            )
        except KeyError:
            return worldcupapp_serializer.MediaSerializer
        media_serializers = {
            "T": worldcupapp_serializer.TextMediaSerializer,
            "I": worldcupapp_serializer.ImageMediaSerializer,
            "G": worldcupapp_serializer.GifMediaSerializer,
            "V": worldcupapp_serializer.VideoMediaSerializer,
        }
        MediaSerializer = media_serializers[worldcup.media_type]
        return MediaSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = worldcupapp_models.Comment.objects.all()
    serializer_class = worldcupapp_serializer.CommentSerializer
