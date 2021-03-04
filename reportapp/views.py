from rest_framework import mixins, viewsets
from reportapp import models as reportapp_models
from reportapp import serializers as reportapp_serializers


class UserReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = reportapp_models.UserReport.objects.all()
    serializer_class = reportapp_serializers.UserReportSerializer
    serializer_action_class = {
        "list": reportapp_serializers.UserReportListSerializer,
        "create": reportapp_serializers.UserReportListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


class WorldcupReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = reportapp_models.WorldcupReport.objects.all()
    serializer_class = reportapp_serializers.WorldcupReportSerializer
    serializer_action_class = {
        "list": reportapp_serializers.WorldcupReportListSerializer,
        "create": reportapp_serializers.WorldcupReportListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


class MediaReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = reportapp_models.MediaReport.objects.all()
    serializer_class = reportapp_serializers.MediaReportSerializer
    serializer_action_class = {
        "list": reportapp_serializers.MediaReportListSerializer,
        "create": reportapp_serializers.MediaReportListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


class CommentReportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = reportapp_models.CommentReport.objects.all()
    serializer_class = reportapp_serializers.CommentReportSerializer
    serializer_action_class = {
        "list": reportapp_serializers.CommentReportListSerializer,
        "create": reportapp_serializers.CommentReportListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class
