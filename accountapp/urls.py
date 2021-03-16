from rest_framework.routers import SimpleRouter
from .views import UserViewSet, ProfileViewSet


router = SimpleRouter()
router.register(prefix="accounts", viewset=UserViewSet, basename="account")
router.register(prefix="profiles", viewset=ProfileViewSet, basename="profile")


urlpatterns = [
    *router.urls,
]
