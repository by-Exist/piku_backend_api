from django.utils.functional import cached_property
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_patchonly_mixin import mixins as dpm_mixins
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..models import Comment, Worldcup
from ..serializers import (
    AnonUserCommentPasswordCheckSerializer,
    CommentPolymorphicDetailSerializer,
    CommentPolymorphicListSerializer,
)


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    dpm_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = CommentPolymorphicDetailSerializer
    serializer_action_class = {
        "list": CommentPolymorphicListSerializer,
        "create": CommentPolymorphicListSerializer,
        "check_password": AnonUserCommentPasswordCheckSerializer,
    }

    @cached_property
    def parent_object(self):
        return get_object_or_404(Worldcup, pk=self.kwargs["worldcup_pk"])

    def get_queryset(self):
        return Comment.objects.filter(worldcup=self.parent_object)

    def get_serializer_class(self):
        if serializer_class := self.serializer_action_class.get(self.action, None):
            return serializer_class
        return self.serializer_class

    @action(methods=["post"], detail=True, url_path="password/check")
    def check_password(self, request, pk=None, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


CommentViewSet = extend_schema_view(
    list=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Comment List",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
    ),
    create=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Comment Create",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
    ),
    partial_update=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Comment Partial Update",
                "- user가 anonymous일 때, 해당 엔드포인트는 check_password 엔드포인트와 함께 사용되어야 한다.",
                "## [ Permission ]",
                "- authenticated = IsWriter",
                "- anonymous = AllowAny",
            ]
        ),
    ),
    destroy=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Comment Destroy",
                "- user가 anonymous일 때, 해당 엔드포인트는 check_password 엔드포인트와 함께 사용되어야 한다.",
                "## [ Permission ]",
                "- authenticated = IsWriter",
                "- anonymous = AllowAny",
            ]
        ),
    ),
    check_password=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Worldcup's Comment Check Password",
                "- 익명 유저의 partial_update, destroy와 동시에 사용되어야 하는 엔드포인트.",
                "- password를 입력받아 해당 익명 댓글의 비밀번호와 동일한지 확인한다.",
                "## [ Permission ]",
                "- Anonymous",
            ]
        ),
        responses={
            204: Response(status=status.HTTP_204_NO_CONTENT),
            400: Response(status=status.HTTP_400_BAD_REQUEST),
        },
    ),
)(CommentViewSet)
