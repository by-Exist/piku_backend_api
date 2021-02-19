from rest_framework import viewsets
from accountapp import models as accountapp_models
from accountapp import serializers as accountapp_serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = accountapp_models.CustomUser.objects.all()
    serializer_class = accountapp_serializers.UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = accountapp_models.Profile.objects.all()
    serializer_class = accountapp_serializers.ProfileSerializer
