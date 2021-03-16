from django.db import models
from rest_framework import serializers
from accountapp.serializers import UserListSerializer

# from rest_framework_nested.relations import NestedHyperlinkedRelatedField


# # Comment Serializer
# class AuthenticatedUserCommentPasswordSerializer(serializers.Serializer):

#     pass


# class AnonymousUserCommentPasswordSerializer(serializers.Serializer):

#     password = serializers.CharField(
#         style={"input_type": "password", "placeholder": "Password"},
#     )


# class CommentSerializer(serializers.HyperlinkedModelSerializer):

#     writer = UserListSerializer(read_only=True)
#     media = MediaListSerializer(read_only=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "id",
#             "comment",
#             "writer",
#             "media",
#             "created_at",
#             "updated_at",
#         )
#         extra_kwargs = {
#             "writer": {"read_only": True},
#             "worldcup": {"read_only": True},
#         }


# class CommentListSerializer(serializers.HyperlinkedModelSerializer):

#     url = NestedHyperlinkedRelatedField(
#         read_only=True,
#         view_name="media-detail",
#         parent_lookup_kwargs={"worldcup_pk": "worldcup__pk"},
#     )
#     writer = UserListSerializer(read_only=True)
#     media = MediaListSerializer(read_only=True)
#     media_id = serializers.IntegerField(write_only=True, allow_null=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "id",
#             "url",
#             "writer",
#             "anonymous_nickname",
#             "comment",
#             "worldcup",
#             "media",
#             "media_id",
#             "created_at",
#             "updated_at",
#         )
#         extra_kwargs = {
#             "writer": {"read_only": True},
#             "worldcup": {"read_only": True},
#             "anonymous_nickname": {"read_only": True},
#         }

#     def create(self, validated_data):
#         user = self.context["request"].user
#         worldcup = worldcupapp_models.Worldcup.objects.get(
#             pk=self.context["view"].kwargs["worldcup_pk"]
#         )
#         validated_data |= {
#             "writer": user,
#             "worldcup": worldcup,
#             "anonymous_nickname": "",
#         }
#         media_id = validated_data.get("media_id")
#         if media_id:
#             media = worldcupapp_models.BaseMedia.objects.get(pk=media_id)
#             validated_data |= {"media": media}
#         return super().create(validated_data)


# class AnonymouseCommentUpdateSerializer(serializers.ModelSerializer):

#     check_password = serializers.CharField(
#         write_only=True,
#         style={"input_type": "password", "placeholder": "Password"},
#     )
#     media_id = serializers.IntegerField(write_only=True, allow_null=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "check_password",
#             "comment",
#             "media_id",
#         )

#     def update(self, instance, validated_data):
#         if "check_password" in validated_data:
#             validated_data.pop("check_password")
#         return super().update(instance, validated_data)


# class AnonymouseCommentCreateSerializer(serializers.ModelSerializer):

#     media_id = serializers.IntegerField(write_only=True, allow_null=True)

#     class Meta:
#         model = worldcupapp_models.Comment
#         fields = (
#             "anonymous_nickname",
#             "anonymous_password",
#             "comment",
#             "media_id",
#         )
#         extra_kwargs = {
#             "anonymous_password": {
#                 "write_only": True,
#                 "style": {"input_type": "password", "placeholder": "Password"},
#             },
#         }

#     def create(self, validated_data):
#         worldcup = worldcupapp_models.Worldcup.objects.get(
#             pk=self.context["view"].kwargs["worldcup_pk"]
#         )
#         validated_data |= {"writer": None, "worldcup": worldcup}
#         media_id = validated_data.get("media_id", None)
#         if media_id:
#             media = worldcupapp_models.BaseMedia.objects.get(pk=media_id)
#             validated_data |= {"media": media}
#         return super().create(validated_data)
