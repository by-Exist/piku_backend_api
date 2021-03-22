from django.utils.functional import cached_property
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from drf_patchonly_mixin import mixins as dpm_mixins
from ..models import Comment, Worldcup
from ..serializers import (
    AuthUserCommentListSerializer,
    AuthUserCommentDetailSerializer,
)


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    dpm_mixins.PatchOnlyMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = AuthUserCommentDetailSerializer
    serializer_action_class = {
        "list": AuthUserCommentListSerializer,
        "create": AuthUserCommentListSerializer,
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
