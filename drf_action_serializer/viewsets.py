from drf_action_serializer.mixins import ActionSerializerMixin
from rest_framework.viewsets import GenericViewSet


class ActionSerializerGenericViewSet(ActionSerializerMixin, GenericViewSet):
    """GenericViewSet과 ActionSerializerMixin을 결합한 클래스입니다."""

    pass