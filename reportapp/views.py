from rest_framework import viewsets
from reportapp import models as reportapp_models
from reportapp import serializers as reportapp_serializers


class ReportViewSet(viewsets.ModelViewSet):
    queryset = reportapp_models.Report.objects.all()
    serializer_class = reportapp_serializers.ReportSerializer
    serializer_action_class = {
        "list": reportapp_serializers.ReportListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class
