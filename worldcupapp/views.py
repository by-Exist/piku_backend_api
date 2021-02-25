from rest_framework import viewsets
from worldcupapp import models as worldcupapp_models
from worldcupapp import serializers as worldcupapp_serializer
import copy


class WorldcupViewSet(viewsets.ModelViewSet):
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


class MediaViewSet(viewsets.ModelViewSet):

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

    def get_queryset(self):
        worldcup_pk = self.kwargs["worldcup_pk"]
        worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
        media_model_cls = self.media_models[worldcup.media_type]
        return media_model_cls.objects.filter(worldcup=worldcup)

    def get_serializer_class(self):
        worldcup_pk = self.kwargs["worldcup_pk"]
        worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
        serializer_cls = self.serializer_action_class[worldcup.media_type].get(
            self.action, None
        )
        if serializer_cls:
            return serializer_cls
        return self.serializer_class[worldcup.media_type]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = worldcupapp_serializer.CommentSerializer
    serializer_action_class = {
        "list": worldcupapp_serializer.CommentListSerializer,
        "create": worldcupapp_serializer.CommentListSerializer,
    }

    def get_queryset(self):
        worldcup_pk = self.kwargs["worldcup_pk"]
        worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
        return worldcupapp_models.Comment.objects.filter(worldcup=worldcup)

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class
