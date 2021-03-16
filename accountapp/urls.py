from django.urls import path
from rest_framework.routers import SimpleRouter
from accountapp.views import UserViewSet, ProfileViewSet
from tokenapp.views import DecoratedTokenObtainPairView, DecoratedTokenRefreshView


router = SimpleRouter()

router.register(prefix="accounts", viewset=UserViewSet, basename="account")
router.register(prefix="profiles", viewset=ProfileViewSet, basename="profile")


urlpatterns = [
    *router.urls,
]
