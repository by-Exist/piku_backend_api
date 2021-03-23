from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedIdentityField
from rest_polymorphic.serializers import PolymorphicSerializer
from ..models import AuthUserComment, AnonUserComment


class AuthUserCommentDetailSerializer(serializers.ModelSerializer):

    nickname = serializers.CharField(read_only=True, source="writer.profile.nickname")
    avatar = serializers.CharField(read_only=True, source="writer.profile.avatar")

    class Meta:
        model = AuthUserComment
        fields = [
            "id",
            "nickname",
            "avatar",
            "media",
            "body",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "media": {"read_only": True},
        }


class AuthUserCommentListSerializer(serializers.ModelSerializer):

    media_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    url = NestedHyperlinkedIdentityField(
        view_name="comment-detail",
        parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
    )
    nickname = serializers.CharField(read_only=True, source="writer.profile.nickname")
    avatar = serializers.CharField(read_only=True, source="writer.profile.avatar")

    class Meta:
        model = AuthUserComment
        fields = [
            "id",
            "url",
            "media_id",
            "nickname",
            "avatar",
            "media",
            "body",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
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


class AnonUserCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonUserComment
        fields = [
            "id",
            "anon_nickname",
            "media",
            "body",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "media": {"read_only": True},
            "anon_nickname": {"read_only": True},
        }


class AnonUserCommentListSerializer(serializers.ModelSerializer):

    media_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    url = NestedHyperlinkedIdentityField(
        view_name="comment-detail",
        parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
    )

    class Meta:
        model = AnonUserComment
        fields = [
            "id",
            "url",
            "media_id",
            "anon_nickname",
            "anon_password",
            "media",
            "body",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "media": {"read_only": True},
            "anon_password": {
                "write_only": True,
                "style": {"input_type": "password"},
            },
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
            "worldcup": self.context["view"].parent_object,
        }
        media_id = validated_data.pop("media_id", None)
        if media_id:
            media = self.context["view"].parent_object.media_set.get(pk=media_id)
            validated_data |= {"media": media}
        return super().create(validated_data)


class AnonUserCommentPasswordCheckSerializer(serializers.Serializer):

    password = serializers.CharField(style={"input_type": "password"})

    def validate_password(self, password):
        comment = self.context["view"].get_object()
        if not (comment.anon_password == password):
            raise serializers.ValidationError("password가 일치하지 않습니다.")
        return password


class CommentPolymorphicDetailSerializer(PolymorphicSerializer):

    model_serializer_mapping = {
        AuthUserComment: AuthUserCommentDetailSerializer,
        AnonUserComment: AnonUserCommentDetailSerializer,
    }


class CommentPolymorphicListSerializer(PolymorphicSerializer):

    resource_type_field_name = "user_type"

    model_serializer_mapping = {
        AuthUserComment: AuthUserCommentListSerializer,
        AnonUserComment: AnonUserCommentListSerializer,
    }

    def get_serializer(self):
        if self.context["request"].user.is_authenticated:
            return (AuthUserCommentListSerializer,)
        return AnonUserCommentListSerializer

    def get_model(self):
        if self.context["request"].user.is_authenticated:
            return AuthUserComment
        return AnonUserComment

    def _get_resource_type_from_mapping(self, mapping):
        return self.get_serializer()

    def _get_serializer_from_resource_type(self, resource_type):
        model = self.get_model()
        return self._get_serializer_from_model_or_instance(model)
