import random
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_action_serializer import mixins as das_mixins
from drf_patchonly_mixin import mixins as dpm_mixins
from . import models as accountapp_models
from . import serializers as accountapp_serializers
from .policys import ProfileViewSetPolicy, UserViewSetAccessPolicy
from .tasks import (
    is_join_sended_token,
    send_mail_to_join_user,
    user_pk_urlsafe_decode,
    send_mail_to_find_password,
    send_mail_to_find_username,
)

# TODO: Response를 어떻게 작성하는지 모르겠다.
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                examples=[
                    OpenApiExample("(None)", value=None),
                    OpenApiExample("date_joined", value="date_joined"),
                    OpenApiExample("-date_joined", value="-date_joined"),
                    OpenApiExample("last_login", value="last_login"),
                    OpenApiExample("-last_login", value="-last_login"),
                ],
            ),
        ],
    ),
)
class UserViewSet(
    das_mixins.ActionSerializerMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    # TODO: Destroy 기능을 어떻게 제공할 것인가?
    # User의 is_active를 False로 변경하는 것으로 만족할 것인가?
    # User 계정의 완전한 제거 기능을 제공하는 것이 올바른가?

    queryset = get_user_model().objects.all().select_related("profile")
    serializer_class = accountapp_serializers.UserDetailSerializer
    serializer_action_class = {
        "list": accountapp_serializers.UserListSerializer,
        "create": accountapp_serializers.UserListSerializer,
        "password": accountapp_serializers.PasswordChangeSerializer,
        "find_username": accountapp_serializers.UsernameFindSerializer,
        "find_password": accountapp_serializers.PasswordFindSerializer,
    }

    permission_classes = [UserViewSetAccessPolicy]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date_joined", "last_login"]

    def perform_create(self, serializer):
        user = serializer.save()
        user = get_user_model().objects.select_related("profile").get(pk=user.pk)
        send_mail_to_join_user(
            request=self.request,
            user=user,
            user_name=user.profile.nickname,
            user_email=user.profile.email,
            view_name="account-active",
        )

    @action(detail=True, methods=["put"])
    def password(self, request, pk=None):
        """user가 자기 자신의 password를 변경하는 엔트포인트."""
        user = self.get_object()
        serializer = self.get_serializer_class()(
            data=request.data, context=self.get_serializer_context()
        )
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=["get"], url_path="active/(?P<uidb64>.+)/(?P<token>.+)"
    )
    def active(self, request, **kwargs):
        """user의 is_active를 True로 변경하는 엔트포인트.\n
        해당 엔드포인트에 접근할 수 있는 url은 user 회원 가입시 이메일로 전송된다.\n
        token과 uidb64 값을 활용해 user를 인식한다."""
        user_pk = user_pk_urlsafe_decode(kwargs["uidb64"])
        token = kwargs["token"]
        user = get_object_or_404(self.get_queryset(), pk=user_pk)
        if is_join_sended_token(user, token):
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"error": "token이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="help/username",
    )
    def find_username(self, request, show_length=4, **kwargs):
        """user가 자신의 id(username)을 분실하였을 경우 사용되는 엔드포인트.\n
        입력받은 email을 사용중인 user가 존재할 경우 email로 username의 일부를 가린 문자열(user****)을 전송한다."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = get_object_or_404(self.get_queryset(), profile__email=email)
            username = user.username
            half_username = username[:show_length] + "*" * (len(username) - show_length)
            send_mail_to_find_username(email, half_username)
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=False,
        methods=["post"],
        url_path="help/password",
    )
    def find_password(self, request, show_length=4, **kwargs):
        """user가 자신의 password를 분실하였을 경우 사용되는 엔드포인트.\n
        입력받은 username, email과 일치하는 user가 존재할 경우 user의 password를 랜덤한 숫자로 변경시키고 email로 해당 숫자를 전송한다."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]
            user = self.get_queryset().get(username=username)
            new_password = str(random.randrange(100000, 1000000))
            user.set_password(new_password)
            user.save()
            send_mail_to_find_password(email, new_password)
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ProfileViewSet(
    mixins.RetrieveModelMixin, dpm_mixins.PatchOnlyMixin, viewsets.GenericViewSet
):
    permission_classes = [ProfileViewSetPolicy]
    queryset = accountapp_models.Profile.objects.all()
    serializer_class = accountapp_serializers.ProfileSerializer
