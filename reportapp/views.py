from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    PolymorphicProxySerializer,
)
from drf_spectacular.types import OpenApiTypes
from drf_patchonly_mixin import mixins as dpm_mixins
from .models import UserReport, WorldcupReport, MediaReport, CommentReport
from .serializers import (
    CommentReportDetailSerializer,
    CommentReportListSerializer,
    MediaReportDetailSerializer,
    MediaReportListSerializer,
    ReportProcessedEditSerializer,
    UserReportDetailSerializer,
    UserReportListSerializer,
    WorldcupReportDetailSerializer,
    WorldcupReportListSerializer,
)
from .policys import ReportViewSetAccessPolicy


class ReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    dpm_mixins.PatchOnlyMixin,
    viewsets.GenericViewSet,
):

    permission_classes = [ReportViewSetAccessPolicy]
    serializer_class = {
        "users": UserReportDetailSerializer,
        "worldcups": WorldcupReportDetailSerializer,
        "medias": MediaReportDetailSerializer,
        "comments": CommentReportDetailSerializer,
    }
    serializer_action_class = {
        "users": {
            "list": UserReportListSerializer,
            "create": UserReportListSerializer,
            "partial_update": ReportProcessedEditSerializer,
        },
        "worldcups": {
            "list": WorldcupReportListSerializer,
            "create": WorldcupReportListSerializer,
            "partial_update": ReportProcessedEditSerializer,
        },
        "medias": {
            "list": MediaReportListSerializer,
            "create": MediaReportListSerializer,
            "partial_update": ReportProcessedEditSerializer,
        },
        "comments": {
            "list": CommentReportListSerializer,
            "create": CommentReportListSerializer,
            "partial_update": ReportProcessedEditSerializer,
        },
    }
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["reason", "processed"]

    queryset_mapping = {
        "users": UserReport.objects.select_related("reporter__profile", "reported"),
        "worldcups": WorldcupReport.objects.select_related(
            "reporter__profile", "reported"
        ),
        "medias": MediaReport.objects.select_related(
            "reporter__profile", "reported__worldcup"
        ),
        "comments": CommentReport.objects.select_related(
            "reporter__profile", "reported__worldcup"
        ),
    }

    def get_queryset(self):
        if self.queryset:
            return self.queryset
        reported_type = self.kwargs["reported_type"]
        self.queryset = self.queryset_mapping[reported_type]
        return self.queryset

    def get_serializer_class(self):
        action = self.action
        reported_type = self.kwargs["reported_type"]
        if serializer_class := self.serializer_action_class.get(reported_type, {}).get(
            action, None
        ):
            return serializer_class
        return self.serializer_class[reported_type]


report_list_serializers = [
    UserReportListSerializer,
    WorldcupReportListSerializer,
    MediaReportListSerializer,
    CommentReportListSerializer,
]

list_polymorphic_proxy_serializer = PolymorphicProxySerializer(
    component_name="ReportList",
    serializers=report_list_serializers,
    resource_type_field_name="pk",  # ???
)

reported_type_path_parameter = OpenApiParameter(
    name="reported_type",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
    required=True,
    examples=[
        OpenApiExample(name="users", value="users"),
        OpenApiExample(name="worldcups", value="worldcups"),
        OpenApiExample(name="medias", value="medias"),
        OpenApiExample(name="comments", value="comments"),
    ],
)

reason_query_paramter = OpenApiParameter(
    name="reason",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
    description="\n\n".join(
        [
            "this query is dependency reported_path_parameter.",
        ]
    ),
    examples=[
        OpenApiExample("{}-{}".format(reported_type, value), "{}".format(name))
        for reported_type, choices in {
            "users": UserReport.Reason.choices,
            "worldcups": WorldcupReport.Reason.choices,
            "medias": MediaReport.Reason.choices,
            "comments": CommentReport.Reason.choices,
        }.items()
        for name, value in choices
    ],
)

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
        responses=list_polymorphic_proxy_serializer,
        parameters=[
            reported_type_path_parameter,
            reason_query_paramter,
            OpenApiParameter(
                name="processed",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                required=False,
                description="this query is filter 'processed'",
            ),
        ],
    ),
    create=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Report Create",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
        parameters=[reported_type_path_parameter],
        request=list_polymorphic_proxy_serializer,
        responses=list_polymorphic_proxy_serializer,
    ),
    partial_update=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Report Partial Update",
                "- only use 'processed' field",
                "## [ Permission ]",
                "- IsSuperUser",
            ]
        ),
        parameters=[reported_type_path_parameter],
        request=ReportProcessedEditSerializer,
        responses={200: ReportProcessedEditSerializer},
    ),
)(ReportViewSet)
