from worldcupapp.models import BaseMedia, Comment, Worldcup
from django.contrib.auth import get_user_model
from reportapp.models import CommentReport, MediaReport, UserReport, WorldcupReport
from worldcupapp.serializers import (
    CommentSerializer,
    MediaSerializer,
    WorldcupSerializer,
)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accountapp.serializers import UserListSerializer, UserSerializer


class AbstractReportSerializer(serializers.ModelSerializer):

    reporter = UserListSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "reporter",
            "reported",
            "reason",
            "body",
            "created_at",
            "image",
        )


class AbstractReportListSerializer(serializers.HyperlinkedModelSerializer):

    reporter = UserListSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "url",
            "reporter",
            "reported",
            "reported_pk",
            "reason",
            "body",
            "image",
            "created_at",
        )

    def validate_reported_pk(self, reported_pk):
        reported_model = self.Meta.reported_model
        if not reported_model.objects.filter(pk=reported_pk).exists():
            raise serializers.ValidationError("신고 대상이 존재하지 않습니다.")
        return reported_pk

    def create(self, validated_data):
        reporter = self.context["request"].user
        if not reporter.is_authenticated:
            reporter = None
        reported_pk = validated_data.pop("reported_pk")
        reported = self.Meta.reported_model.objects.get(pk=reported_pk)
        validated_data |= {"reporter": reporter, "reported": reported}
        return super().create(validated_data)


class UserReportSerializer(AbstractReportSerializer):

    reported = UserSerializer(read_only=True)

    class Meta(AbstractReportSerializer.Meta):
        model = UserReport


class UserReportListSerializer(AbstractReportListSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="report-user-detail")
    reported = UserSerializer(read_only=True)
    reported_pk = serializers.IntegerField(write_only=True)

    class Meta(AbstractReportListSerializer.Meta):
        model = UserReport
        reported_model = get_user_model()


class WorldcupReportSerializer(AbstractReportSerializer):

    reported = WorldcupSerializer(read_only=True)

    class Meta(AbstractReportSerializer.Meta):
        model = WorldcupReport


class WorldcupReportListSerializer(AbstractReportListSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="report-worldcup-detail")
    reported = WorldcupSerializer(read_only=True)
    reported_pk = serializers.IntegerField(write_only=True)

    class Meta(AbstractReportListSerializer.Meta):
        model = WorldcupReport
        reported_model = Worldcup


class MediaReportSerializer(AbstractReportSerializer):

    reported = MediaSerializer(read_only=True)

    class Meta(AbstractReportSerializer.Meta):
        model = MediaReport


class MediaReportListSerializer(AbstractReportListSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="report-media-detail")
    reported = MediaSerializer(read_only=True)
    reported_pk = serializers.IntegerField(write_only=True)

    class Meta(AbstractReportListSerializer.Meta):
        model = MediaReport
        reported_model = BaseMedia


class CommentReportSerializer(AbstractReportSerializer):

    reported = CommentSerializer(read_only=True)

    class Meta(AbstractReportSerializer.Meta):
        model = CommentReport


class CommentReportListSerializer(AbstractReportListSerializer):

    url = serializers.HyperlinkedIdentityField(view_name="report-comment-detail")
    reported = CommentSerializer(read_only=True)
    reported_pk = serializers.IntegerField(write_only=True)

    class Meta(AbstractReportListSerializer.Meta):
        model = CommentReport
        reported_model = Comment
