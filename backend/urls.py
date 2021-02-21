from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt import views as simplejwt_views
from accountapp import views as accountapp_views
from worldcupapp import views as worldcupapp_views

router = routers.DefaultRouter()
router.register("accounts", accountapp_views.UserViewSet)
router.register("profile", accountapp_views.ProfileViewSet)
router.register("worldcups", worldcupapp_views.WorldcupViewSet)
worldcup_router = routers.NestedDefaultRouter(router, "worldcups", lookup="worldcup")
worldcup_router.register("medias", worldcupapp_views.MediaViewSet, basename="medias")
worldcup_router.register(
    "comments", worldcupapp_views.CommentViewSet, basename="comments"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(worldcup_router.urls)),
    path(
        "token/",
        simplejwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        simplejwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
