import random
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)
from django_filters.rest_framework import DjangoFilterBackend
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


# TODO: User의 회원 탈퇴 기능 구현을 고민해야 한다. Delete로 퉁 칠 것인가? is_active를 False로 변환할 것인가?
class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = get_user_model().objects.all().select_related("profile")
    serializer_class = accountapp_serializers.UserDetailSerializer
    serializer_action_class = {
        "list": accountapp_serializers.UserListSerializer,
        "create": accountapp_serializers.UserListSerializer,
        "password": accountapp_serializers.UserPasswordSerializer,
        "find_username": accountapp_serializers.UserFindUsernameSerializer,
        "find_password": accountapp_serializers.UserFindPasswordSerializer,
    }

    permission_classes = [UserViewSetAccessPolicy]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["date_joined", "last_login"]
    filterset_fields = ["is_superuser", "is_active"]
    search_fields = ["username", "profile__nickname"]

    @action(
        detail=True,
        methods=["put"],
    )
    def password(self, request, pk=None):
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
        detail=False,
        methods=["get"],
        url_path="active/(?P<uidb64>.+)/(?P<token>.+)",
    )
    def active(self, request, **kwargs):
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

    def get_serializer_class(self):
        if serializer_class := self.serializer_action_class.get(self.action, None):
            return serializer_class
        return self.serializer_class

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


UserViewSet = extend_schema_view(
    list=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Account List",
                "## [ Permission ]",
                "- AllowAny",
            ]
        ),
        parameters=[
            OpenApiParameter(
                name="ordering",
                examples=[
                    OpenApiExample("--", value=None),
                    *[
                        OpenApiExample(f"asc {field_name}", value=f"{field_name}")
                        for field_name in UserViewSet.ordering_fields
                    ],
                    *[
                        OpenApiExample(f"desc {field_name}", value=f"-{field_name}")
                        for field_name in UserViewSet.ordering_fields
                    ],
                ],
            ),
            OpenApiParameter(
                name="is_active",
                description="사용자 활성화 여부",
            ),
            OpenApiParameter(
                name="is_superuser",
                description="사용자 superuser 여부",
            ),
            OpenApiParameter(
                name="search",
                description="username, nickname",
            ),
        ],
    ),
    create=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Account Create",
                "## [ Permission ]",
                "- Anonymous",
            ]
        )
    ),
    retrieve=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Account Retrieve",
                "## [ Permission ]",
                "- AllowAny",
            ]
        )
    ),
    password=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Password Change",
                "- User가 자신의 비밀번호를 변경할 때 사용한다.",
                "## [ Permission ]",
                "- IsSelf",
            ]
        ),
    ),
    active=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Account Active",
                "- 회원가입이 끝나면 해당 엔드포인트로 접근할 수 있는 url이 user의 이메일로 전송된다.",
                "- url path 내의 token과 user id를 활용하여 해당 user의 is_active를 True로 변환한다.",
                "## [ Permission ]",
                "- Anonymous",
            ]
        ),
    ),
    find_username=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Find Username",
                "- id(username)을 분실하였을 경우 사용되는 엔드포인트.",
                "- 입력받은 email을 사용중인 user가 존재할 경우 해당 email로 username의 일부를 가린 문자열(user****)을 전송한다.",
                "## [ Permission ]",
                "- Anonymous",
            ]
        ),
    ),
    find_password=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Find Password",
                "- password를 분실하였을 경우 사용되는 엔드포인트.",
                "- 입력받은 username, email과 일치하는 user가 존재할 경우 user의 password를 랜덤한 숫자(100000~999999)로 변경시키고 email로 해당 숫자를 전송한다.",
                "## [ Permission ]",
                "- Anonymous",
            ]
        ),
    ),
)(UserViewSet)


class ProfileViewSet(
    mixins.RetrieveModelMixin, dpm_mixins.PatchOnlyMixin, viewsets.GenericViewSet
):
    permission_classes = [ProfileViewSetPolicy]
    queryset = accountapp_models.Profile.objects.all()
    serializer_class = accountapp_serializers.ProfileDetailSerializer


ProfileViewSet = extend_schema_view(
    retrieve=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Profile Retrieve",
                "## [ Permission ]",
                "- IsSelf",
            ]
        ),
    ),
    partial_update=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Profile Partial Update",
                "## [ Permission ]",
                "- IsSelf",
            ]
        ),
    ),
)(ProfileViewSet)
