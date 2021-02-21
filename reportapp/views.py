from rest_framework import viewsets
from reportapp import models as reportapp_models
from reportapp import serializers as reportapp_serializers


class ReportViewSet(viewsets.ModelViewSet):
    queryset = reportapp_models.Report.objects.all()
    serializer_class = reportapp_serializers.ReportSerializer
