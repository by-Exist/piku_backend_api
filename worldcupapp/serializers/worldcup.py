from rest_framework import serializers
from accountapp.serializers import UserListSerializer
from ..models import Worldcup


class WorldcupDetailSerializer(serializers.ModelSerializer):

    creator = UserListSerializer(read_only=True)

    class Meta:
        model = Worldcup
        fields = (
            "id",
            "title",
            "subtitle",
            "media_type",
            "publish_type",
            "password",
            "view_count",
            "play_count",
            "created_at",
            "updated_at",
            "creator",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate_publish_type(self, publish_type):
        if publish_type in (
            Worldcup.PublishType.PUBLIC.value,
            Worldcup.PublishType.PASSWORD.value,
        ):
            if not self.context["view"].get_object().media_set.count() >= 2:
                return publish_type
            raise serializers.ValidationError("최소 2개 이상의 media를 업로드 해 주세요.")
        return publish_type


class WorldcupListSerializer(serializers.HyperlinkedModelSerializer):

    creator = UserListSerializer(read_only=True)

    class Meta:
        model = Worldcup
        fields = (
            "id",
            "url",
            "title",
            "subtitle",
            "media_type",
            "publish_type",
            "creator",
        )
        extra_kwargs = {
            "creator": {"read_only": True},
            "media_type": {"required": True},
            "publish_type": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data |= {"creator": self.context["view"].request.user}
        return super().create(validated_data)


class NoBodyPostSerializer(serializers.Serializer):

    pass
