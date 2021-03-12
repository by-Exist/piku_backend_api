from django.urls import path
from rest_framework.routers import SimpleRouter
from accountapp.views import (
    UserViewSet,
    ProfileViewSet,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
)


router = SimpleRouter()

router.register(prefix="accounts", viewset=UserViewSet, basename="account")
# router.register(prefix="profiles", viewset=ProfileViewSet, basename="profile")


urlpatterns = [
    *router.urls,
    # path(
    #     "token/",
    #     DecoratedTokenObtainPairView.as_view(),
    #     name="token_obtain_pair",
    # ),
    # path(
    #     "token/refresh/",
    #     DecoratedTokenRefreshView.as_view(),
    #     name="token_refresh",
    # ),
]
