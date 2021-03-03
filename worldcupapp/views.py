from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from worldcupapp import models as worldcupapp_models
from worldcupapp import serializers as worldcupapp_serializer
from backend import mixins as backend_mixins


class WorldcupViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    backend_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = worldcupapp_models.Worldcup.objects.all()
    serializer_class = worldcupapp_serializer.WorldcupSerializer
    serializer_action_class = {
        "list": worldcupapp_serializer.WorldcupListSerializer,
        "create": worldcupapp_serializer.WorldcupListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    backend_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    media_models = {
        "T": worldcupapp_models.TextMedia,
        "I": worldcupapp_models.ImageMedia,
        "G": worldcupapp_models.GifMedia,
        "V": worldcupapp_models.VideoMedia,
    }
    serializer_class = {
        "T": worldcupapp_serializer.TextMediaSerializer,
        "I": worldcupapp_serializer.ImageMediaSerializer,
        "G": worldcupapp_serializer.GifMediaSerializer,
        "V": worldcupapp_serializer.VideoMediaSerializer,
    }
    serializer_action_class = {
        "T": {
            "list": worldcupapp_serializer.TextMediaListSerializer,
            "create": worldcupapp_serializer.TextMediaListSerializer,
        },
        "I": {
            "list": worldcupapp_serializer.ImageMediaListSerializer,
            "create": worldcupapp_serializer.ImageMediaListSerializer,
        },
        "G": {
            "list": worldcupapp_serializer.GifMediaListSerializer,
            "create": worldcupapp_serializer.GifMediaListSerializer,
        },
        "V": {
            "list": worldcupapp_serializer.VideoMediaListSerializer,
            "create": worldcupapp_serializer.VideoMediaListSerializer,
        },
    }

    # TODO: action - score-board [get], queryset anotate 기능 활용

    def get_queryset(self):
        worldcup_pk = self.kwargs.get("worldcup_pk")
        if not worldcup_pk:
            return worldcupapp_models.BaseMedia.objects.none()
        worldcup = get_object_or_404(worldcupapp_models.Worldcup, pk=worldcup_pk)
        media_model_cls = self.media_models[worldcup.media_type]
        return media_model_cls.objects.filter(worldcup=worldcup)

    def get_serializer_class(self):
        worldcup_pk = self.kwargs.get("worldcup_pk", None)
        if not worldcup_pk:
            return worldcupapp_serializer.MediaSerializer
        try:
            worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
        except worldcupapp_models.Worldcup.DoesNotExist:
            return worldcupapp_serializer.MediaSerializer
        serializer_cls = self.serializer_action_class[worldcup.media_type].get(
            self.action, None
        )
        if serializer_cls:
            return serializer_cls
        return self.serializer_class[worldcup.media_type]

    def perform_destroy(self, instance):
        instance = worldcupapp_models.BaseMedia.objects.get(pk=instance.id)
        instance.delete()


class CommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    backend_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = worldcupapp_serializer.CommentSerializer
    serializer_action_class = {
        "list": worldcupapp_serializer.CommentListSerializer,
        "create": worldcupapp_serializer.CommentListSerializer,
    }

    def get_queryset(self):
        worldcup_pk = self.kwargs.get("worldcup_pk", None)
        if not worldcup_pk:
            return worldcupapp_models.Comment.objects.none()
        worldcup = get_object_or_404(worldcupapp_models.Worldcup, pk=worldcup_pk)
        return worldcupapp_models.Comment.objects.filter(worldcup=worldcup)

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class
