from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from worldcupapp import models as worldcupapp_models
from worldcupapp import serializers as worldcupapp_serializer
from drf_patchonly_mixin import mixins as dpm_mixins

# from .policys import (
#     WorldcupViewSetAccessPolicy,
#     # CommentViewSetAccessPolicy,
#     # MediaViewSetAccessPolicy,
# )


# from .policys import (
#     WorldcupViewSetAccessPolicy,
#     # CommentViewSetAccessPolicy,
#     # MediaViewSetAccessPolicy,
# )

# class CommentViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     dpm_mixins.PatchOnlyMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet,
# ):
#     permission_classes = [CommentViewSetAccessPolicy]
#     serializer_class = worldcupapp_serializer.CommentListSerializer
#     serializer_action_class = {
#         "authenticated": {
#             "list": worldcupapp_serializer.CommentListSerializer,
#             "create": worldcupapp_serializer.CommentListSerializer,
#             "check_writer": worldcupapp_serializer.AuthenticatedUserCommentPasswordSerializer,
#         },
#         "anonymous": {
#             "create": worldcupapp_serializer.AnonymouseCommentCreateSerializer,
#             "partial_update": worldcupapp_serializer.AnonymouseCommentUpdateSerializer,
#             "check_writer": worldcupapp_serializer.AnonymousUserCommentPasswordSerializer,
#         },
#     }

#     @action(detail=True, methods=["post"])
#     def check_writer(self, request, **kwargs):
#         """
#         ### login 중일 경우\n
#         - password 입력 X\n
#         - comment의 writer가 login user임을 확인하고 맞으면 200, 아니면 405 반환\n
#         ### login 하지 않은 경우\n
#         - password 입력 O\n
#         - comment의 anonymous_password가 password와 동일함을 확인하고 맞으면 200, 아니면 405 반환
#         """
#         allow = Response(status=status.HTTP_200_OK)
#         deny = Response(status=status.HTTP_403_FORBIDDEN)
#         user = request.user
#         comment = self.get_object()
#         if user.is_authenticated:
#             if comment.writer == user:
#                 return allow
#             return deny
#         else:
#             serializer = self.get_serializer_class()(data=request.data)
#             if serializer.is_valid():
#                 if comment.anonymous_password == serializer.validated_data["password"]:
#                     return allow
#                 return deny
#             return deny

#     def get_queryset(self):
#         worldcup_pk = self.kwargs.get("worldcup_pk", None)
#         if not worldcup_pk:
#             return worldcupapp_models.Comment.objects.none()
#         worldcup = get_object_or_404(worldcupapp_models.Worldcup, pk=worldcup_pk)
#         return worldcupapp_models.Comment.objects.filter(worldcup=worldcup)

#     def get_serializer_class(self):
#         user = self.request.user
#         user_type = "authenticated" if user.is_authenticated else "anonymous"
#         if self.action in self.serializer_action_class[user_type]:
#             return self.serializer_action_class[user_type][self.action]
#         return self.serializer_class
