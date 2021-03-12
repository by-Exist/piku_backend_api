class ActionSerializerMixin:
    """
    해당 믹스인은 GenericAPIView 및 서브클래스에 활용할 수 있습니다.
    해당 믹스인은 get_serializer_class를 확장합니다.
    선택적으로 클래스 속성 serializer_action_class를 요구합니다.
    일반적인 사용 방식은 다음과 같습니다.

    serializer_class = DetailSerializer
    serializer_action_class = {
        "list": ListSerializer,
        "create": ListSerializer,
        "action_method_name": ActionUseSerializer,
    }

    동작방식
    serializer_action_class 속성이 없다면 self.serializer_class를 반환합니다.
    self.action 속성을 활용하여 serializer_action_class를 조회하며,
    일치하는 serializer class가 있다면 해당 시리얼라이저 클래스를 반환합니다.
    일치하는 serializer class가 없다면 self.serializer_class를 반환합니다.
    """

    def get_serializer_class(self):
        if not hasattr(self, "serializer_action_class"):
            return self.serializer_class
        serializer_cls = self.serializer_action_class.get(self.action, None)
        if serializer_cls:
            return serializer_cls
        return self.serializer_class
