from rest_framework import serializers
from reportapp import models as reportapp_models


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = reportapp_models.Report
        fields = "__all__"
