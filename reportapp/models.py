from worldcupapp.models import Worldcup, Media, Comment
from django.db import models
from django.contrib.auth import get_user_model
from polymorphic.models import PolymorphicModel


class Report(PolymorphicModel):

    reporter = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="신고자",
    )
    body = models.CharField("신고 내용", blank=True, max_length=511)
    image = models.ImageField(
        "증빙 사진", blank=True, upload_to="reportapp/report/%Y/%m/%d"
    )
    created_at = models.DateTimeField("작성일", auto_now_add=True)


class UserReport(Report):
    class Reason(models.TextChoices):
        USEREXAMPLE = "USEREXAMPLE", "유저 신고 사유 예제"

    reported = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="신고된 유저"
    )
    reason = models.CharField("신고 사유", max_length=15, choices=Reason.choices)


class WorldcupReport(Report):
    class Reason(models.TextChoices):
        WORLDCUPEXAMPLE = "WORLDCUPEXAMPLE", "월드컵 신고 사유 예제"

    reported = models.ForeignKey(
        Worldcup, on_delete=models.CASCADE, verbose_name="신고된 월드컵"
    )
    reason = models.CharField("신고 사유", max_length=15, choices=Reason.choices)


class MediaReport(Report):
    class Reason(models.TextChoices):
        MEDIAEXAMPLE = "MEDIAEXAMPLE", "미디어 신고 사유 예제"

    reported = models.ForeignKey(
        Media, on_delete=models.CASCADE, verbose_name="신고된 미디어"
    )
    reason = models.CharField("신고 사유", max_length=15, choices=Reason.choices)


class CommentReport(Report):
    class Reason(models.TextChoices):
        COMMENTEXAMPLE = "COMMENTEXAMPLE", "댓글 신고 사유 예제"

    reported = models.ForeignKey(
        Comment, on_delete=models.CASCADE, verbose_name="신고된 댓글"
    )
    reason = models.CharField("신고 사유", max_length=15, choices=Reason.choices)
