from django.shortcuts import get_object_or_404
from accountapp.tasks.email import (
    send_mail_to_find_password,
    send_mail_to_find_username,
)
from django.contrib.auth import get_user_model
from rest_framework import status, mixins, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt import views as simplejwt_views
from drf_spectacular.utils import extend_schema
from drf_action_serializer.mixins import ActionSerializerMixin
from backend.mixins import PatchOnlyMixin
from accountapp import models as accountapp_models
from accountapp.policys import ProfileViewSetPolicy, UserViewSetAccessPolicy
from accountapp import serializers as accountapp_serializers
from accountapp.tasks import (
    is_join_sended_token,
    send_mail_to_join_user,
    user_pk_urlsafe_decode,
)
import random


class UserViewSet(
    ActionSerializerMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

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

    @action(detail=True, methods=["patch"])
    def password(self, request, pk=None):
        # 유저가 자신의 password를 변경하는데에 사용된다.
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
        # 회원가입 시 이메일로 전송된 url로 전송하면 is_active를 True로 변경한다.
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
        # email로 username의 힌트를 전송한다.
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
        # email로 변경된 password를 전송한다.
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
    mixins.RetrieveModelMixin, PatchOnlyMixin, viewsets.GenericViewSet
):
    permission_classes = [ProfileViewSetPolicy]
    queryset = accountapp_models.Profile.objects.all()
    serializer_class = accountapp_serializers.ProfileSerializer


class DecoratedTokenObtainPairView(simplejwt_views.TokenObtainPairView):
    @extend_schema(
        responses={200: accountapp_serializers.TokenObtainPairResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(simplejwt_views.TokenRefreshView):
    @extend_schema(
        responses={200: accountapp_serializers.TokenRefreshResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
