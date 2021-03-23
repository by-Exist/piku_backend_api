from rest_framework.routers import SimpleRouter
from .views import ReportViewSet


router = SimpleRouter()

router.register("reports", ReportViewSet, "report")

urlpatterns = router.urls
