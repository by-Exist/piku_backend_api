from rest_framework import viewsets
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
