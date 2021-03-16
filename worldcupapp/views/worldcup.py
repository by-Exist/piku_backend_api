from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from worldcupapp import models as worldcupapp_models
from worldcupapp import serializers as worldcupapp_serializer
from drf_patchonly_mixin import mixins as dpm_mixins
from ..policys import WorldcupViewSetAccessPolicy

# CommentViewSetAccessPolicy,
# MediaViewSetAccessPolicy,


class WorldcupViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    dpm_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [WorldcupViewSetAccessPolicy]
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
