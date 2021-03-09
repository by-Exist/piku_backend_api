from worldcupapp.models import BaseMedia, Comment, Worldcup
from django.db import models
from django.contrib.auth import get_user_model


# Report Model
class AbstractReport(models.Model):
    class CommonReason(models.TextChoices):
        ADULT = "Sex", "성적 요소가 포함되어 있습니다."
        HATE = "Hate", "증오/혐오 등의 내용이 포함되어 있습니다."
        SPAM = "Spam", "스팸 및 광고성 내용이 포함되어 있습니다."
        CHILD_ABUSE = "Child", "아동학대 관련 내용이 포함되어 있습니다."
        OTHER = "Other", "기타"

    reporter = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="신고자",
    )
    reason = models.CharField("신고 사유", max_length=15, choices=CommonReason.choices)
    body = models.CharField("신고 내용", blank=True, max_length=511)
    image = models.ImageField(
        "증빙 사진", blank=True, upload_to="reportapp/report/%Y/%m/%d"
    )
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    class Meta:
        abstract = True


class UserReport(AbstractReport):
    reported = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="유저", related_name="+"
    )


class WorldcupReport(AbstractReport):
    reported = models.ForeignKey(Worldcup, on_delete=models.CASCADE, verbose_name="월드컵")


class MediaReport(AbstractReport):
    reported = models.ForeignKey(
        BaseMedia, on_delete=models.CASCADE, verbose_name="미디어"
    )


class CommentReport(AbstractReport):
    reported = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="댓글")
