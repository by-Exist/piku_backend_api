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
    }

    permission_classes = [UserViewSetAccessPolicy]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date_joined", "last_login"]

    def perform_create(self, serializer):
        user = serializer.save()
        user = get_user_model().objects.get(pk=user).select_related("profile")
        send_mail_to_join_user(
            request=self.request,
            user=user,
            user_name=user.profile.nickname,
            user_email=user.profile.email,
            view_name="account-active",
        )

    # TODO: 이 것과, 아랫 것의 extend_schema를 ViewSet에 등록하도록 옮기자.
    @extend_schema(
        description="""회원가입 시 이메일로 전송되는 링크. user의 is_active를 True로 전환하는 엔드포인트""",
        responses={200: None},
    )
    @action(
        detail=False, methods=["get"], url_path="active/(?P<uidb64>.+)/(?P<token>.+)"
    )
    def active(self, request, **kwargs):
        user_pk = user_pk_urlsafe_decode(kwargs["uidb64"])
        token = kwargs["token"]
        try:
            user = get_user_model().objects.get(pk=user_pk)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "유저가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        if is_join_sended_token(user, token):
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"error": "token이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        description="유저가 직접 자기 계정의 패스워드를 변경할 때 사용하는 엔드포인트",
        responses={204: None},
    )
    @action(detail=True, methods=["patch"])
    def password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer_class()(
            data=request.data, context=self.get_serializer_context()
        )
        if serializer.is_valid():
            user.set_password(serializer.data["new_password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
