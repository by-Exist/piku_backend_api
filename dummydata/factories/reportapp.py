import factory
from random import choice
from reportapp.models import UserReport, WorldcupReport, MediaReport, CommentReport


class AbstractReportFactory(factory.django.DjangoModelFactory):
    body = factory.Sequence(lambda n: "({}) 신고 내용...".format(n))
    # image = factory.LazyFunction(
    #     lambda: factory.Faker("image_url") if choice([True, False]) else None
    # )

    class Meta:
        abstract = True


class UserReportFactory(AbstractReportFactory):
    reason = UserReport.Reason.USEREXAMPLE

    class Meta:
        model = UserReport


class WorldcupReportFactory(AbstractReportFactory):
    reason = WorldcupReport.Reason.WORLDCUPEXAMPLE

    class Meta:
        model = WorldcupReport


class MediaReportFactory(AbstractReportFactory):
    reason = MediaReport.Reason.MEDIAEXAMPLE

    class Meta:
        model = MediaReport


class CommentReportFactory(AbstractReportFactory):
    reason = CommentReport.Reason.COMMENTEXAMPLE

    class Meta:
        model = CommentReport
