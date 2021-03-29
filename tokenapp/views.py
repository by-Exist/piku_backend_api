from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.settings import api_settings
from drf_spectacular.utils import extend_schema, extend_schema_view


class DecoratedTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


DecoratedTokenObtainPairView = extend_schema_view(
    post=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Obtain Token",
                f"- Access Token Lifetime = {api_settings.ACCESS_TOKEN_LIFETIME}",
                f"- Refresh Token Lifetime = {api_settings.REFRESH_TOKEN_LIFETIME}",
                "## [ Permission ]",
                "- AllowAny",
            ]
        )
    )
)(DecoratedTokenObtainPairView)


DecoratedTokenRefreshView = extend_schema_view(
    post=extend_schema(
        description="\n\n".join(
            [
                "## [ Description ]",
                "- Refresh Token",
                "## [ Permission ]",
                "- AllowAny",
            ]
        )
    )
)(DecoratedTokenRefreshView)
