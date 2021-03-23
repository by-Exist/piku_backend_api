from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from worldcupapp.models import Worldcup, Media, Comment
from .models import UserReport, WorldcupReport, MediaReport, CommentReport


# List Serializers
class ReportListSerializer(serializers.ModelSerializer):

    mapping = {
        UserReport: get_user_model(),
        WorldcupReport: Worldcup,
        MediaReport: Media,
        CommentReport: Comment,
    }

    reported_pk = serializers.IntegerField(write_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="report-detail")

    class Meta:
        fields = [
            "id",
            "url",
            "reporter",
            "reported_pk",
            "reported",
            "reason",
            "body",
            "image",
            "created_at",
        ]
        extra_kwargs = {
            "reporter": {"read_only": True},
            "reported": {"read_only": True},
        }

    def validate_reported_pk(self, reported_pk):
        report_model = self.Meta.model
        if not self.mapping[report_model].objects.filter(pk=reported_pk).exists():
            raise serializers.ValidationError(
                f"{self.mapping[report_model].__name__}에 해당 객체가 존재하지 않습니다."
            )
        return reported_pk

    def create(self, validated_data):
        reported_pk = validated_data.pop("reported_pk")
        reported = self.mapping[self.Meta.model].objects.get(pk=reported_pk)
        reporter = self.context["request"].user
        validated_data |= {
            "reported": reported,
            "reporter": reporter if reporter.is_authenticated else None,
        }
        return super().create(validated_data)


class UserReportListSerializer(ReportListSerializer):

    reported = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="account-detail"
    )

    class Meta(ReportListSerializer.Meta):
        model = UserReport


class WorldcupReportListSerializer(ReportListSerializer):

    reported = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="worldcup-detail"
    )

    class Meta(ReportListSerializer.Meta):
        model = WorldcupReport


class MediaReportListSerializer(ReportListSerializer):

    reported = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name="media-detail",
        parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
    )

    class Meta(ReportListSerializer.Meta):
        model = MediaReport


class CommentReportListSerializer(ReportListSerializer):

    reported = NestedHyperlinkedRelatedField(
        read_only=True,
        view_name="comment-detail",
        parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
    )

    class Meta(ReportListSerializer.Meta):
        model = CommentReport


class ReportPolymorphicListSerializer(PolymorphicSerializer):

    resource_type_field_name = "reported_type"

    model_serializer_mapping = {
        UserReport: UserReportListSerializer,
        WorldcupReport: WorldcupReportListSerializer,
        MediaReport: MediaReportListSerializer,
        CommentReport: CommentReportListSerializer,
    }


# Detail Serializers
class UserReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReport
        fields = [
            "id",
            "reporter",
            "reported",
            "reason",
            "body",
            "image",
            "created_at",
        ]


class WorldcupReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldcupReport
        fields = [
            "id",
            "reporter",
            "reported",
            "reason",
            "body",
            "image",
            "created_at",
        ]


class MediaReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaReport
        fields = [
            "id",
            "reporter",
            "reported",
            "reason",
            "body",
            "image",
            "created_at",
        ]


class CommentReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = [
            "id",
            "reporter",
            "reported",
            "reason",
            "body",
            "image",
            "created_at",
        ]


class ReportPolymorphicDetailSerializer(PolymorphicSerializer):

    resource_type_field_name = "reported_type"

    model_serializer_mapping = {
        UserReport: UserReportDetailSerializer,
        WorldcupReport: WorldcupReportDetailSerializer,
        MediaReport: MediaReportDetailSerializer,
        CommentReport: CommentReportDetailSerializer,
    }
