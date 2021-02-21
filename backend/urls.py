from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_nested import routers
from rest_framework_simplejwt import views as simplejwt_views
from accountapp import views as accountapp_views
from worldcupapp import views as worldcupapp_views
from reportapp import views as reportapp_views

router = routers.DefaultRouter()
router.register("accounts", accountapp_views.UserViewSet)
router.register("profile", accountapp_views.ProfileViewSet)
router.register("worldcups", worldcupapp_views.WorldcupViewSet)
worldcup_router = routers.NestedDefaultRouter(router, "worldcups", lookup="worldcup")
worldcup_router.register("medias", worldcupapp_views.MediaViewSet, basename="medias")
worldcup_router.register(
    "comments", worldcupapp_views.CommentViewSet, basename="comments"
)
router.register("reports", reportapp_views.ReportViewSet)

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

    schema_view = get_schema_view(
        openapi.Info(
            title="Dev Backend API",
            default_version="v1",
            description="백엔드 개발 환경에서 활용될 API 문서입니다.",
            # terms_of_service="https://www.google.com/policies/terms/",
            # contact=openapi.Contact(email="contact@snippets.local"),
            # license=openapi.License(name="BSD License"),
        ),
        # 사용자가 접근 가능한 엔드포인트만 보여주고 싶다면 False로 설정
        public=True,
        # authentication_classes=(),
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = [
        *urlpatterns,
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
