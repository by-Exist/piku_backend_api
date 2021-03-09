from rest_framework import mixins, viewsets
from reportapp import models as reportapp_models
from reportapp.policys import ReportViewSetAccessPolicy
from reportapp.serializers import (
    CommentReportListSerializer,
    CommentReportSerializer,
    MediaReportListSerializer,
    MediaReportSerializer,
    UserReportListSerializer,
    UserReportSerializer,
    WorldcupReportListSerializer,
    WorldcupReportSerializer,
)


class ReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    모든 Report에서 공통적으로 사용되는 메서드와 상속 관계를 위해 작성된 뷰셋
    상속을 통해 활용한다.
    """

    permission_classes = [ReportViewSetAccessPolicy]

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


class UserReportViewSet(ReportViewSet):
    """Report - User"""

    queryset = reportapp_models.UserReport.objects.all()
    serializer_class = UserReportSerializer
    serializer_action_class = {
        "list": UserReportListSerializer,
        "create": UserReportListSerializer,
    }


class WorldcupReportViewSet(ReportViewSet):
    """Report - Worldcup"""

    queryset = reportapp_models.WorldcupReport.objects.all()
    serializer_class = WorldcupReportSerializer
    serializer_action_class = {
        "list": WorldcupReportListSerializer,
        "create": WorldcupReportListSerializer,
    }


class MediaReportViewSet(ReportViewSet):
    """Report - Media"""

    queryset = reportapp_models.MediaReport.objects.all()
    serializer_class = MediaReportSerializer
    serializer_action_class = {
        "list": MediaReportListSerializer,
        "create": MediaReportListSerializer,
    }


class CommentReportViewSet(ReportViewSet):
    """Report - Comment"""

    queryset = reportapp_models.CommentReport.objects.all()
    serializer_class = CommentReportSerializer
    serializer_action_class = {
        "list": CommentReportListSerializer,
        "create": CommentReportListSerializer,
    }
