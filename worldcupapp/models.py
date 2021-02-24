from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class Worldcup(models.Model):
    class MediaType(models.TextChoices):
        TEXT = "T", "Text"
        IMAGE = "I", "Image"
        GIF = "G", "Gif"
        Video = "V", "Image"

    class PublishType(models.TextChoices):
        PUBLIC = "PUBLIC", "공개"
        PRIVATE = "PRIVATE", "비공개"
        PASSWORD = "PASSWORD", "암호"

    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(
        "제목", max_length=63, validators=[MinLengthValidator(10, "열 글자 이상 입력해주세요.")]
    )
    subtitle = models.CharField("부제", max_length=511)
    media_type = models.CharField(
        "미디어 타입", max_length=1, choices=MediaType.choices, default=MediaType.IMAGE
    )
    publish_type = models.CharField("배포 방식", max_length=8, choices=PublishType.choices)
    password = models.CharField(
        "암호",
        blank=True,
        max_length=12,
        validators=[MinLengthValidator(3, "여덟 글자 이상 입력해주세요.")],
    )
    created_at = models.DateTimeField("작성시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정시각", auto_now=True)
    play_count = models.PositiveIntegerField("플레이 완료 횟수", blank=True, default=0)

    def get_absolute_url(self):
        return reverse("worldcup-detail", args=[self.id])


# 테이블을 만드는 용도로 사용되며, 직접적으로 활용되지는 않음
class BaseMedia(models.Model):
    worldcup = models.ForeignKey(Worldcup, on_delete=models.CASCADE, verbose_name="월드컵")
    title = models.CharField("제목", max_length=31)
    media = models.CharField("미디어", max_length=511)
    win_count = models.PositiveIntegerField("승리 횟수", blank=True, default=0)
    choice_count = models.PositiveIntegerField("1:1 선택 횟수", blank=True, default=0)

    def get_absolute_url(self):
        return reverse("media-detail", args=[self.id])

    class Meta:
        db_table = "Medias"


class AbstractMedia(models.Model):
    worldcup = models.ForeignKey(Worldcup, on_delete=models.CASCADE, verbose_name="월드컵")
    title = models.CharField("제목", max_length=31)
    win_count = models.PositiveIntegerField("승리 횟수", blank=True, default=0)
    choice_count = models.PositiveIntegerField("1:1 선택 횟수", blank=True, default=0)

    class Meta:
        abstract = True


class TextMedia(AbstractMedia):
    media = models.CharField("Text 미디어", max_length=511)

    class Meta:
        db_table = "Medias"
        managed = False


class ImageMedia(AbstractMedia):
    media = models.ImageField(
        "Image 미디어", upload_to="worldcupapp/imagemedia/%Y/%m/%d/%H"
    )

    class Meta:
        db_table = "Medias"
        managed = False


class GifMedia(AbstractMedia):
    media = models.ImageField("Gif 미디어", upload_to="worldcupapp/imagemedia/%Y/%m/%d/%H")

    class Meta:
        db_table = "Medias"
        managed = False


class VideoMedia(AbstractMedia):
    media = models.CharField("텍스트 미디어", max_length=255)

    class Meta:
        db_table = "Medias"
        managed = False


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    worldcup = models.ForeignKey(Worldcup, on_delete=models.CASCADE, verbose_name="월드컵")
    media = models.ForeignKey(
        BaseMedia, null=True, blank=True, on_delete=models.CASCADE, verbose_name="미디어"
    )
    comment = models.CharField("댓글 내용", max_length=511)

    def get_absolute_url(self):
        return reverse("comment-detail", args=[self.id])
