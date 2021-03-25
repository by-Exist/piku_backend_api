from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from worldcupapp.models.worldcup import Worldcup
from rest_framework import mixins, viewsets, response, status
from rest_framework.decorators import action
from drf_spectacular.utils import (
    PolymorphicProxySerializer,
    extend_schema_view,
    extend_schema,
)
from drf_patchonly_mixin import mixins as dpm_mixins
from ..models import Media
from ..policys import MediaViewSetAccessPolicy
from ..serializers import (
    GifMediaDetailSerializer,
    GifMediaListSerializer,
    ImageMediaDetailSerializer,
    ImageMediaListSerializer,
    TextMediaDetailSerializer,
    TextMediaListSerializer,
    VideoMediaDetailSerializer,
    VideoMediaListSerializer,
    MediaCountListSerializer,
)


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    dpm_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

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

    @cached_property
    def parent_object(self):
        return get_object_or_404(Worldcup, pk=self.kwargs["worldcup_pk"])

    def get_queryset(self):
        return Media.objects.filter(worldcup=self.parent_object)

    def get_serializer_class(self):
        if self.action == "counts":
            return MediaCountListSerializer
        if self.action in ("create", "list"):
            return self.list_serializer_class[self.parent_object.media_type]
        return self.detail_serializer_class[self.parent_object.media_type]

    @action(methods=["patch"], detail=False)
    def counts(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            medias = self.get_queryset()
            for counts_data in serializer.validated_data["counts"]:
                media_id = counts_data["media_id"]
                if up_win_count := counts_data.get("up_win_count", None):
                    medias.get(pk=media_id).win_count_up(up_win_count)
                if up_view_count := counts_data.get("up_view_count", None):
                    medias.get(pk=media_id).view_count_up(up_view_count)
                if up_choice_count := counts_data.get("up_choice_count", None):
                    medias.get(pk=media_id).choice_count_up(up_choice_count)
            Media.objects.bulk_update(
                medias, ["win_count", "view_count", "choice_count"]
            )
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


MediaListPolymorphicSerializer = PolymorphicProxySerializer(
    component_name="MediaListPolymorphic",
    serializers=[
        TextMediaListSerializer,
        ImageMediaListSerializer,
        GifMediaListSerializer,
        VideoMediaListSerializer,
    ],
    resource_type_field_name=None,
)
MediaDetailPolymorphicSerializer = PolymorphicProxySerializer(
    component_name="MediaDetailPolymorphic",
    serializers=[
        TextMediaDetailSerializer,
        ImageMediaDetailSerializer,
        GifMediaDetailSerializer,
        VideoMediaDetailSerializer,
    ],
    resource_type_field_name=None,
)


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
        request=MediaDetailPolymorphicSerializer,
        responses=MediaDetailPolymorphicSerializer,
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
    ),
    counts=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Media's view counts Update",
                "- 게임이 종료될 때 사용된 미디어들의 정보 업데이트에 사용",
                "- media의 win_count, view_count, choice_count를 대상으로 함",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
        responses={
            200: None,
            400: None,
        },
    ),
)(MediaViewSet)