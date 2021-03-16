from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator


class Worldcup(models.Model):
    class MediaType(models.TextChoices):
        TEXT = "Text", "텍스트"
        IMAGE = "Image", "이미지"
        GIF = "Gif", "움짤"
        Video = "Video", "외부 비디오 링크"

    class PublishType(models.TextChoices):
        PUBLIC = "PUBLIC", "공개"
        PRIVATE = "PRIVATE", "비공개"
        PASSWORD = "PASSWORD", "암호"

    creator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="작성자"
    )
    title = models.CharField(
        "제목", max_length=63, validators=[MinLengthValidator(3, "세 글자 이상 입력해주세요.")]
    )
    subtitle = models.CharField("부제", max_length=511)
    media_type = models.CharField(
        "미디어 타입", max_length=15, choices=MediaType.choices, default=MediaType.IMAGE
    )
    publish_type = models.CharField(
        "배포 방식", max_length=8, choices=PublishType.choices, default=PublishType.PRIVATE
    )
    password = models.CharField(
        "암호",
        blank=True,
        max_length=12,
        validators=[MinLengthValidator(3, "여덟 글자 이상 입력해주세요.")],
    )
    created_at = models.DateTimeField("작성시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정시각", auto_now=True)
    play_count = models.PositiveIntegerField(
        "플레이 완료 횟수", blank=True, default=0, editable=False
    )