from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_action_serializer.viewsets import ActionSerializerGenericViewSet
from accountapp.policys import UserViewSetAccessPolicy
from accountapp.serializers import (
    UserDetailSerializer,
    UserListSerializer,
    PasswordChangeSerializer,
)

# TODO: 다른 모듈로 분리하는 것이 적절한 것 같다.
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


account_activation_token = AccountActivationTokenGenerator()


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    ActionSerializerGenericViewSet,
):

    permission_classes = [UserViewSetAccessPolicy]
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailSerializer
    serializer_action_class = {
        "list": UserListSerializer,
        "create": UserListSerializer,
        "password": PasswordChangeSerializer,
    }

    # TODO: 좀 더 깔끔하게 정리할 방법이 없을까?
    def perform_create(self, serializer):
        user = serializer.save()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        url_rel = reverse("account-active", args=[uidb64, token])
        url_abs = self.request.build_absolute_uri(url_rel)
        mail_title = "이메일 인증을 완료해주세요."
        mail_body = f"아래 링크를 클릭하면 회원가입이 완료됩니다.\nLink : {url_abs}"
        mail_from = "bolk9652@gmail.com"
        mail_to = serializer.validated_data["email"]
        send_mail(mail_title, mail_body, from_email=mail_from, recipient_list=[mail_to])

    # TODO: 이 것과, 아랫 것의 extend_schema를 ViewSet에 등록하도록 옮기자.
    @extend_schema(
        description="""회원가입 시 이메일로 전송되는 링크. user의 is_active를 True로 전환""",
        responses={200: None},
    )
    @action(
        detail=False, methods=["get"], url_path="active/(?P<uidb64>.+)/(?P<token>.+)"
    )
    def active(self, request, **kwargs):
        uidb64 = kwargs["uidb64"]
        user_pk = force_text(urlsafe_base64_decode(uidb64))
        token = kwargs["token"]
        try:
            user = get_user_model().objects.get(pk=user_pk)
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "해당 유저를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"error": "유효하지 않은 token으로 접근하였습니다."}, status=status.HTTP_400_BAD_REQUEST
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
