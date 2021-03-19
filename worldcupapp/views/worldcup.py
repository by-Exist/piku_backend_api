from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes
from drf_patchonly_mixin import mixins as dpm_mixins
from ..models import Worldcup
from ..policys import WorldcupViewSetAccessPolicy
from ..serializers import (
    WorldcupDetailSerializer,
    WorldcupListSerializer,
    NoBodyPostSerializer,
)


class WorldcupViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    dpm_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [WorldcupViewSetAccessPolicy]
    queryset = Worldcup.objects.all()
    serializer_class = WorldcupDetailSerializer
    serializer_action_class = {
        "list": WorldcupListSerializer,
        "create": WorldcupListSerializer,
        "play_counts": NoBodyPostSerializer,
        "view_counts": NoBodyPostSerializer,
    }

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["media_type", "publish_type"]
    search_fields = ["title", "subtitle"]
    ordering_fields = ["created_at", "play_count"]

    # TODO: 캐싱 동작을 구현하여, 응답을 202와 204로 분리하자.
    @action(methods=["post"], detail=True)
    def view_counts(self, request, **kwargs):
        worldcup = self.get_object()
        worldcup.view_count = F("view_count") + 1
        worldcup.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO: 캐싱 동작을 구현하여, 응답을 202와 204로 분리하자.
    @action(methods=["post"], detail=True)
    def play_counts(self, request, **kwargs):
        worldcup = self.get_object()
        worldcup.play_count = F("play_count") + 1
        worldcup.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


WorldcupViewSet = extend_schema_view(
    list=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup List",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
        parameters=[
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                examples=[
                    OpenApiExample("--", None),
                    *[
                        OpenApiExample(f"asc {field_name}", f"{field_name}")
                        for field_name in WorldcupViewSet.ordering_fields
                    ],
                    *[
                        OpenApiExample(f"desc {field_name}", f"-{field_name}")
                        for field_name in WorldcupViewSet.ordering_fields
                    ],
                ],
            )
        ],
    ),
    create=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup Create",
                "## [ Permission ]",
                "- Authenticated",
            ]
        )
    ),
    retrieve=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup Retrieve",
                "## [ Permission ]",
                "- AllowAny",
            ]
        )
    ),
    partial_update=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup Partial Update",
                "## [ Permission ]",
                "- IsCreator",
            ]
        )
    ),
    destroy=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup Destroy",
                "## [ Permission ]",
                "- IsCreator",
            ]
        )
    ),
    play_counts=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup Play Counts +1",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
        responses={204: NoBodyPostSerializer},
    ),
    view_counts=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup View Counts +1",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
        responses={204: NoBodyPostSerializer},
    ),
)(WorldcupViewSet)
