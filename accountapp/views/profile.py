from rest_framework import viewsets, mixins
from accountapp import models as accountapp_models
from accountapp import serializers as accountapp_serializers
from backend.mixins import PatchOnlyMixin
from accountapp.policys import ProfileViewSetPolicy


class ProfileViewSet(
    mixins.RetrieveModelMixin, PatchOnlyMixin, viewsets.GenericViewSet
):
    permission_classes = [ProfileViewSetPolicy]
    queryset = accountapp_models.Profile.objects.all()
    serializer_class = accountapp_serializers.ProfileSerializer
