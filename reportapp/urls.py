from rest_framework.routers import SimpleRouter
from .views import ReportViewSet


router = SimpleRouter()

reported_type_str_list = ["users", "worldcups", "medias", "comments"]

router.register(
    "reports/(?P<reported_type>(" + "|".join(reported_type_str_list) + "))",
    ReportViewSet,
    "report",
)

urlpatterns = router.urls
