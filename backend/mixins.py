from rest_framework.mixins import UpdateModelMixin


class PatchOnlyMixin(object):
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return UpdateModelMixin.update(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
