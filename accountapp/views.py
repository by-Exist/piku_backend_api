from rest_framework import viewsets
from rest_framework_simplejwt import views as simplejwt_views
from drf_spectacular.utils import extend_schema
from accountapp import models as accountapp_models
from accountapp import serializers as accountapp_serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = accountapp_models.CustomUser.objects.all()
    serializer_class = accountapp_serializers.UserSerializer
    serializer_action_class = {
        "list": accountapp_serializers.UserListSerializer,
        "create": accountapp_serializers.UserListSerializer,
    }

    def get_serializer_class(self):
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class


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
