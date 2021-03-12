class ActionSerializerMixin:
    def get_serializer_class(self):
        if not hasattr(self, "serializer_action_class"):
            return self.serializer_class
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class
