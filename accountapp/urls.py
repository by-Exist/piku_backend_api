from django.urls import path
from rest_framework.routers import SimpleRouter
from accountapp.views import (
    UserViewSet,
    ProfileViewSet,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
)


router = SimpleRouter()

router.register("accounts", UserViewSet, "account")
router.register("profiles", ProfileViewSet, "profile")


urlpatterns = [
    *router.urls,
    path(
        "token/",
        DecoratedTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        DecoratedTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
