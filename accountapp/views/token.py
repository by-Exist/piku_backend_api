from rest_framework_simplejwt import views as simplejwt_views
from drf_spectacular.utils import extend_schema
from accountapp.serializers import (
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
)


class DecoratedTokenObtainPairView(simplejwt_views.TokenObtainPairView):
    @extend_schema(responses={200: TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(simplejwt_views.TokenRefreshView):
    @extend_schema(responses={200: TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
