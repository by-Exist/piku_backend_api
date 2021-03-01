from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt import views as simplejwt_views
from drf_spectacular.utils import extend_schema
from accountapp import models as accountapp_models
from accountapp import serializers as accountapp_serializers
from accountapp.tokens import account_activation_token


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = accountapp_models.CustomUser.objects.all()
    serializer_class = accountapp_serializers.UserSerializer
    serializer_action_class = {
        "list": accountapp_serializers.UserListSerializer,
        "create": accountapp_serializers.UserListSerializer,
        "password": accountapp_serializers.PasswordChangeSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class

    def perform_create(self, serializer):
        user = serializer.save()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        url_rel = reverse("customuser-active", args=[uidb64, token])
        url_abs = self.request.build_absolute_uri(url_rel)
        mail_title = "이메일 인증을 완료해주세요."
        mail_body = f"아래 링크를 클릭하면 회원가입이 완료됩니다.\nLink : {url_abs}"
        mail_from = "bolk9652@gmail.com"
        mail_to = serializer.validated_data["email"]
        send_mail(mail_title, mail_body, from_email=mail_from, recipient_list=[mail_to])

    @extend_schema(responses={200: None})
    @action(
        detail=False, methods=["get"], url_path="active/(?P<uidb64>.+)/(?P<token>.+)"
    )
    def active(self, request, **kwargs):
        """회원가입을 완료 후, 이메일로 전송된 링크로 접근하여
        user의 is_active를 True로 전환하는 엔드포인트"""
        uidb64 = kwargs["uidb64"]
        user_pk = force_text(urlsafe_base64_decode(uidb64))
        token = kwargs["token"]
        try:
            user = accountapp_models.CustomUser.objects.get(pk=user_pk)
        except accountapp_models.CustomUser.DoesNotExist:
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

    @extend_schema(responses={200: None})
    @action(detail=True, methods=["put"])
    def password(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data["new_password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = accountapp_models.Profile.objects.all()
    serializer_class = accountapp_serializers.ProfileSerializer
    serializer_action_class = {
        "list": accountapp_serializers.ProfileListSerializer,
        "create": accountapp_serializers.ProfileListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


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
