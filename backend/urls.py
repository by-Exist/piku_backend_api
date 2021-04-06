from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("", include("accountapp.urls")),
    path("", include("tokenapp.urls")),
    path("", include("worldcupapp.urls")),
    path("", include("reportapp.urls")),
    # SpectacularRedocView나 SpectacularSwaggerView는
    # SpectacularAPIView를 필요로 한다. (url_name)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:

    import debug_toolbar

    static_urlpatterns = [
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]

    debug_toolbar_urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    rest_framework_auth_urlpatterns = [
        path("api-auth/", include("rest_framework.urls")),
    ]

    schema_urlpatterns = [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

    urlpatterns = [
        *urlpatterns,
        path("", include(schema_urlpatterns)),
        path("", include(static_urlpatterns)),
        path("", include(debug_toolbar_urlpatterns)),
        path("", include(rest_framework_auth_urlpatterns)),
    ]
