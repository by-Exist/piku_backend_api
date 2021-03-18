from worldcupapp.serializers import (
    GifMediaDetailSerializer,
    GifMediaListSerializer,
    ImageMediaDetailSerializer,
    ImageMediaListSerializer,
    TextMediaDetailSerializer,
    TextMediaListSerializer,
    VideoMediaDetailSerializer,
    VideoMediaListSerializer,
)
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from worldcupapp.models.worldcup import Worldcup
from rest_framework import mixins, viewsets
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)
from drf_patchonly_mixin import mixins as dpm_mixins
from ..models import Media
from ..serializers import (
    MediaDetailPolymorphicSerializer,
    MediaListPolymorphicSerializer,
)
from ..policys import MediaViewSetAccessPolicy


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    dpm_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = MediaDetailPolymorphicSerializer
    type_serializer_class = {""}
    detail_serializer_class = {
        "Text": TextMediaDetailSerializer,
        "Image": ImageMediaDetailSerializer,
        "Gif": GifMediaDetailSerializer,
        "Video": VideoMediaDetailSerializer,
    }
    list_serializer_class = {
        "Text": TextMediaListSerializer,
        "Image": ImageMediaListSerializer,
        "Gif": GifMediaListSerializer,
        "Video": VideoMediaListSerializer,
    }
    permission_classes = [MediaViewSetAccessPolicy]

    def get_queryset(self):
        return Media.objects.filter(worldcup=self.parent_object)

    def get_serializer_class(self):
        if self.action in ("create", "list"):
            return self.list_serializer_class[self.parent_object.media_type]
        return self.detail_serializer_class[self.parent_object.media_type]

    @cached_property
    def parent_object(self):
        return get_object_or_404(Worldcup, pk=self.kwargs["worldcup_pk"])


MediaViewSet = extend_schema_view(
    list=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Media List",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
        request=MediaListPolymorphicSerializer,
        responses=MediaListPolymorphicSerializer,
    ),
    create=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Media Create",
                "## [ Permission ]",
                "- IsWorldcupCreator",
            ]
        ),
        request=MediaListPolymorphicSerializer,
        responses=MediaListPolymorphicSerializer,
    ),
    partial_update=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Media Partial Update",
                "## [ Permission ]",
                "- IsWorldcupCreator",
            ]
        ),
        request=MediaListPolymorphicSerializer,
        responses=MediaListPolymorphicSerializer,
    ),
    destroy=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Media Destroy",
                "## [ Permission ]",
                "- IsWorldcupCreator",
            ]
        ),
        request=MediaListPolymorphicSerializer,
        responses=MediaListPolymorphicSerializer,
    ),
)(MediaViewSet)
