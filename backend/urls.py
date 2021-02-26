from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular import views as spectacular_views
from rest_framework_nested import routers
from accountapp import views as accountapp_views
from worldcupapp import views as worldcupapp_views
from reportapp import views as reportapp_views
import debug_toolbar

router = routers.DefaultRouter()
router.register("accounts", accountapp_views.UserViewSet)
router.register("profile", accountapp_views.ProfileViewSet)
router.register("worldcups", worldcupapp_views.WorldcupViewSet)
worldcup_router = routers.NestedDefaultRouter(router, "worldcups", lookup="worldcup")
worldcup_router.register("medias", worldcupapp_views.MediaViewSet, basename="media")
worldcup_router.register(
    "comments", worldcupapp_views.CommentViewSet, basename="comment"
)
router.register("reports", reportapp_views.ReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(worldcup_router.urls)),
    path(
        "token/",
        accountapp_views.DecoratedTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        accountapp_views.DecoratedTokenRefreshView.as_view(),
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
        path(
            "api/schema/", spectacular_views.SpectacularAPIView.as_view(), name="schema"
        ),
        path(
            "api/schema/swagger-ui/",
            spectacular_views.SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            spectacular_views.SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
        path("__debug__/", include(debug_toolbar.urls)),
    ]
