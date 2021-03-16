from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
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
from ..serializers import WorldcupDetailSerializer, WorldcupListSerializer


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
    }

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["media_type", "publish_type"]
    search_fields = ["title", "subtitle"]
    ordering_fields = ["created_at", "play_count"]

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
)(WorldcupViewSet)
