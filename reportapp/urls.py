from django.conf import settings
from rest_framework.routers import SimpleRouter
from reportapp.views import (
    CommentReportViewSet,
    MediaReportViewSet,
    UserReportViewSet,
    WorldcupReportViewSet,
)

router = SimpleRouter()

router.register("reports/users", UserReportViewSet, "report-user")
router.register("reports/worldcups", WorldcupReportViewSet, "report-worldcup")
router.register("reports/medias", MediaReportViewSet, "report-media")
router.register("reports/comments", CommentReportViewSet, "report-comment")

urlpatterns = router.urls
