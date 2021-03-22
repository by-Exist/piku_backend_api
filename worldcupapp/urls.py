from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from worldcupapp.views import WorldcupViewSet, MediaViewSet, CommentViewSet


router = SimpleRouter()

router.register("worldcups", WorldcupViewSet, "worldcup")
worldcup_router = NestedSimpleRouter(router, "worldcups", lookup="worldcup")
worldcup_router.register("medias", MediaViewSet, "media")
worldcup_router.register("comments", CommentViewSet, "comment")

urlpatterns = [
    *router.urls,
    *worldcup_router.urls,
]
