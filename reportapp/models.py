from django.db import models
from django.contrib.auth import get_user_model


class Report(models.Model):
    class ReportedTargetType(models.TextChoices):
        USER = "User", "유저"
        WORLDCUP = "Worldcup", "월드컵"
        MEDIA = "Media", "미디어"
        COMMENT = "Comment", "댓글"

    class Reason(models.TextChoices):
        ADULT = "Adult", "성적 요소"
        HATE = "Hate", "혐오"
        SPAM = "Spam", "스팸 및 광고"
        CHILD_ABUSE = "Child Abuse", "아동학대"
        OTHER = "Other", "기타"

    reporter = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="신고자",
    )
    target_type = models.CharField(
        "신고 대상 유형", choices=ReportedTargetType.choices, max_length=10
    )
    target_id = models.PositiveIntegerField("신고 대상 id")
    reason = models.CharField("신고 사유", choices=Reason.choices, max_length=16)
    report = models.CharField("신고 내용", blank=True, max_length=511)
    image = models.ImageField(
        "증빙 사진", blank=True, upload_to="reportapp/report/%Y/%m/%d"
    )
    created_at = models.DateTimeField("작성일", auto_now_add=True)

    class Meta:
        unique_together = ("target_type", "target_id")
