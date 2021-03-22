from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedIdentityField
from ..models import AuthUserComment


class AuthUserCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserComment
        fields = [
            "id",
            "writer",
            "media",
            "body",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "writer": {"read_only": True},
            "media": {"read_only": True},
        }


class AuthUserCommentListSerializer(serializers.ModelSerializer):

    media_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    url = NestedHyperlinkedIdentityField(
        view_name="comment-detail",
        parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
    )

    class Meta:
        model = AuthUserComment
        fields = [
            "id",
            "url",
            "media_id",
            "writer",
            "media",
            "body",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "writer": {"read_only": True},
            "media": {"read_only": True},
        }

    def validate_media_id(self, media_id):
        if not media_id:
            return media_id
        media_set = self.context["view"].parent_object.media_set
        if media_id and (not media_set.filter(pk=media_id).exists()):
            raise serializers.ValidationError("월드컵에 해당 미디어가 존재하지 않습니다.")
        return media_id

    def create(self, validated_data):
        validated_data |= {
            "writer": self.context["request"].user,
            "worldcup": self.context["view"].parent_object,
        }
        media_id = validated_data.pop("media_id", None)
        if media_id:
            media = self.context["view"].parent_object.media_set.get(pk=media_id)
            validated_data |= {"media": media}
        return super().create(validated_data)
