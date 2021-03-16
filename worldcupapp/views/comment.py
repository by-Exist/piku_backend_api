from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from worldcupapp import models as worldcupapp_models
from worldcupapp import serializers as worldcupapp_serializer
from drf_patchonly_mixin import mixins as dpm_mixins

# from .policys import (
#     WorldcupViewSetAccessPolicy,
#     # CommentViewSetAccessPolicy,
#     # MediaViewSetAccessPolicy,
# )


# class MediaViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     dpm_mixins.PatchOnlyMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet,
# ):

#     media_models = {
#         "Text": worldcupapp_models.TextMedia,
#         "Image": worldcupapp_models.ImageMedia,
#         "Gif": worldcupapp_models.GifMedia,
#         "Video": worldcupapp_models.VideoMedia,
#     }
#     serializer_class = {
#         "Text": worldcupapp_serializer.TextMediaSerializer,
#         "Image": worldcupapp_serializer.ImageMediaSerializer,
#         "Gif": worldcupapp_serializer.GifMediaSerializer,
#         "Video": worldcupapp_serializer.VideoMediaSerializer,
#     }
#     serializer_action_class = {
#         "Text": {
#             "list": worldcupapp_serializer.TextMediaListSerializer,
#             "create": worldcupapp_serializer.TextMediaListSerializer,
#         },
#         "Image": {
#             "list": worldcupapp_serializer.ImageMediaListSerializer,
#             "create": worldcupapp_serializer.ImageMediaListSerializer,
#         },
#         "Gif": {
#             "list": worldcupapp_serializer.GifMediaListSerializer,
#             "create": worldcupapp_serializer.GifMediaListSerializer,
#         },
#         "Video": {
#             "list": worldcupapp_serializer.VideoMediaListSerializer,
#             "create": worldcupapp_serializer.VideoMediaListSerializer,
#         },
#     }

#     permission_classes = [MediaViewSetAccessPolicy]

#     # TODO: action - score-board [get], queryset anotate 기능 활용

#     def get_queryset(self):
#         worldcup_pk = self.kwargs.get("worldcup_pk")
#         if not worldcup_pk:
#             return worldcupapp_models.BaseMedia.objects.none()
#         worldcup = get_object_or_404(worldcupapp_models.Worldcup, pk=worldcup_pk)
#         media_model_cls = self.media_models[worldcup.media_type]
#         return media_model_cls.objects.filter(worldcup=worldcup)

#     def get_serializer_class(self):
#         worldcup_pk = self.kwargs.get("worldcup_pk", None)
#         if not worldcup_pk:
#             return worldcupapp_serializer.MediaSerializer
#         try:
#             worldcup = worldcupapp_models.Worldcup.objects.get(pk=worldcup_pk)
#         except worldcupapp_models.Worldcup.DoesNotExist:
#             return worldcupapp_serializer.MediaSerializer
#         serializer_cls = self.serializer_action_class[worldcup.media_type].get(
#             self.action, None
#         )
#         if serializer_cls:
#             return serializer_cls
#         return self.serializer_class[worldcup.media_type]

#     def perform_destroy(self, instance):
#         instance = worldcupapp_models.BaseMedia.objects.get(pk=instance.id)
#         instance.delete()
