import factory
from random import choice
from worldcupapp.models import (
    Worldcup,
    TextMedia,
    ImageMedia,
    GifMedia,
    VideoMedia,
    AuthUserComment,
    AnonUserComment,
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


class AbstractMediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    title = factory.Sequence(lambda n: "미디어 제목({})".format(n))


class TextMediaFactory(AbstractMediaFactory):
    class Meta:
        model = TextMedia

    body = factory.Faker("paragraph")


class ImageMediaFactory(AbstractMediaFactory):
    class Meta:
        model = ImageMedia

    body = factory.Faker("image_url")


class GifMediaFactory(AbstractMediaFactory):
    class Meta:
        model = GifMedia

    body = factory.Faker("image_url")


class VideoMediaFactory(AbstractMediaFactory):
    class Meta:
        model = VideoMedia

    body = factory.Faker("image_url")


class AbstractCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    body = factory.Sequence(lambda n: "댓글 내용 ({})".format(n))


class AuthUserCommentFactory(AbstractCommentFactory):
    class Meta:
        model = AuthUserComment


class AnonUserCommentFactory(AbstractCommentFactory):

    anon_nickname = factory.Sequence(lambda n: "익명 닉네임 ({})".format(n))
    anon_password = "password"

    class Meta:
        model = AnonUserComment
