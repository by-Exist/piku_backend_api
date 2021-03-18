from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from worldcupapp.models.worldcup import Worldcup
from worldcupapp.serializers.media import (
    GifMediaListSerializer,
    ImageMediaListSerializer,
    TextMediaListSerializer,
    VideoMediaListSerializer,
)
from rest_framework import mixins
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    PolymorphicProxySerializer,
)
from drf_spectacular.types import OpenApiTypes
from drf_action_serializer import viewsets as das_viewsets
from drf_patchonly_mixin import mixins as dpm_mixins
from ..models import Media
from ..serializers import (
    MediaDetailPolymorphicSerializer,
    MediaListPolymorphicSerializer,
)


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    dpm_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    das_viewsets.ActionSerializerGenericViewSet,
):

    serializer_class = MediaDetailPolymorphicSerializer
    serializer_action_class = {
        "list": MediaListPolymorphicSerializer,
        "create": MediaListPolymorphicSerializer,
    }

    def get_queryset(self):
        print(self.parent_object._meta.model)
        return Media.objects.filter(worldcup=self.parent_object)

    @cached_property
    def parent_object(self):
        return get_object_or_404(Worldcup, pk=self.kwargs["worldcup_pk"])


MediaViewSet = extend_schema_view()(MediaViewSet)
