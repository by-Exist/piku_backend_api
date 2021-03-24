import factory
import tempfile
from random import choice
from worldcupapp.models import Worldcup, TextMedia, ImageMedia, GifMedia, VideoMedia


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


class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    title = factory.Sequence(lambda n: "미디어 제목({})".format(n))


class TextMediaFactory(MediaFactory):
    class Meta:
        model = TextMedia

    body = factory.Faker("paragraph")


class ImageMediaFactory(MediaFactory):
    class Meta:
        model = ImageMedia

    body = factory.Faker("image_url")


class GifMediaFactory(MediaFactory):
    class Meta:
        model = GifMedia

    body = factory.Faker("image_url")


class VideoMediaFactory(MediaFactory):
    class Meta:
        model = VideoMedia

    body = factory.Faker("image_url")
