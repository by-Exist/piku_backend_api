from rest_framework import serializers
from reportapp import models as reportapp_models
from accountapp import models as accountapp_models
from worldcupapp import models as worldcupapp_models


class TargetUrlMethodMixin:
    def get_target_url(self, obj):
        MODELS = {
            "User": accountapp_models.CustomUser,
            "Worldcup": worldcupapp_models.Worldcup,
            "Media": worldcupapp_models.BaseMedia,
            "Comment": worldcupapp_models.Comment,
        }
        target_obj = MODELS[obj.target_type].objects.get(pk=obj.target_id)
        request = self.context["view"].request
        return request.build_absolute_uri(target_obj.get_absolute_url())


# TODO: report의 수정이 필요한가? 필요 없는 과정일 것 같은데...
class ReportSerializer(TargetUrlMethodMixin, serializers.ModelSerializer):

    target_url = serializers.SerializerMethodField(method_name="get_target_url")

    class Meta:
        model = reportapp_models.Report
        fields = (
            "id",
            "target_url",
            "target_type",
            "target_id",
            "reason",
            "report",
            "image",
            "reporter",
        )
        extra_kwargs = {
            "reporter": {"read_only": True},
            "target_type": {"read_only": True},
            "target_id": {"read_only": True},
        }

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ReportListSerializer(
    TargetUrlMethodMixin, serializers.HyperlinkedModelSerializer
):

    target_url = serializers.SerializerMethodField(method_name="get_target_url")

    class Meta:
        model = reportapp_models.Report
        fields = (
            "id",
            "url",
            "target_url",
            "target_type",
            "target_id",
            "reason",
            "report",
            "image",
            "reporter",
        )
        extra_kwargs = {
            "reporter": {"read_only": True},
            "target_id": {"write_only": True},
            "target_type": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data |= {"reporter": self.context["view"].request.user}
        return super().create(validated_data)
