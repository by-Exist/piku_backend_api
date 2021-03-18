from polymorphic.models import PolymorphicModel
from django.db import models
from ..models import Worldcup


class Media(PolymorphicModel):
    worldcup = models.ForeignKey(
        Worldcup, on_delete=models.CASCADE, verbose_name="월드컵", related_name="media_set"
    )
    title = models.CharField("제목", max_length=31)
    win_count = models.PositiveIntegerField(
        "승리 횟수", blank=True, default=0, editable=False
    )
    view_count = models.PositiveBigIntegerField(
        "등장 횟수", blank=True, default=0, editable=False
    )
    choice_count = models.PositiveIntegerField(
        "선택 횟수", blank=True, default=0, editable=False
    )


class TextMedia(Media):
    body = models.TextField("텍스트", max_length=1023)


class ImageMedia(Media):
    body = models.ImageField("이미지", upload_to="worldcup/media/image/%Y/%m/%d/%H")


class GifMedia(Media):
    body = models.FileField("움짤", upload_to="worldcup/media/gif/%Y/%m/%d/%H")


class VideoMedia(Media):
    body = models.CharField("외부 동영상 링크", max_length=255)
