import factory
from random import choice
from worldcupapp.models import (
    Worldcup,
)


class WorldcupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Worldcup

    title = factory.Sequence(lambda n: "테스트 월드컵({})".format(n))
    subtitle = factory.Sequence(lambda n: "테스트 월드컵({}) 입니다.".format(n))
    media_type = factory.LazyFunction(lambda: choice(Worldcup.MediaType.values))
    publish_type = factory.LazyFunction(lambda: choice(Worldcup.PublishType.values))
    password = factory.LazyAttribute(
        lambda obj: "password" if obj.publish_type == "PASSWORD" else ""
    )
