from django.db.models import Prefetch
from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from .policys import ReportViewSetAccessPolicy
from .serializers import (
    ReportPolymorphicDetailSerializer,
    ReportPolymorphicListSerializer,
)
from .models import Report, UserReport, WorldcupReport, MediaReport, CommentReport


class ReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = [ReportViewSetAccessPolicy]
    serializer_class = ReportPolymorphicDetailSerializer
    serializer_action_class = {
        "list": ReportPolymorphicListSerializer,
        "create": ReportPolymorphicListSerializer,
    }

    def get_queryset(self):
        return (
            Report.objects.select_related("reporter")
            .prefetch_related(
                Prefetch(
                    "reported",
                    Report.objects.instance_of(UserReport).all()
                    | Report.objects.instance_of(WorldcupReport).all()
                    | Report.objects.instance_of(MediaReport).all()
                    | Report.objects.instance_of(CommentReport).all(),
                )
            )
            .all()
        )

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


ReportViewSet = extend_schema_view(
    list=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Report List",
                "## [ Permission ]",
                "- IsSuperUser",
            ]
        ),
    ),
    create=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Report Create",
                "## [ Permission ]",
                "- AllowAny",
                "## [ Polymorphic Field ]",
                '- reported_type = Union["UserReport", "WorldcupReport", "MediaReport", "CommentReport"]',
            ]
        )
    ),
    destroy=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Report Destroy",
                "## [ Permission ]",
                "- IsSuperUser",
            ]
        )
    ),
)(ReportViewSet)
