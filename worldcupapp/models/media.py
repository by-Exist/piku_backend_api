from polymorphic.models import PolymorphicModel
from django.db import models
from ..models import Worldcup


# polymorphic 모델의 계단식 삭제가 올바르게 적용되지 않는 문제 해결
# https://github.com/django-polymorphic/django-polymorphic/issues/229
def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class Media(PolymorphicModel):
    worldcup = models.ForeignKey(
        Worldcup,
        on_delete=NON_POLYMORPHIC_CASCADE,
        verbose_name="월드컵",
        related_name="media_set",
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

    def win_count_up(self, num):
        """no save"""
        self.win_count = models.F("win_count") + num

    def view_count_up(self, num):
        """no save"""
        self.view_count = models.F("view_count") + num

    def choice_count_up(self, num):
        """no save"""
        self.choice_count = models.F("choice_count") + num


class TextMedia(Media):
    body = models.TextField("텍스트", max_length=1023)


class ImageMedia(Media):
    body = models.ImageField("이미지", upload_to="worldcup/media/image/%Y/%m/%d/%H")


class GifMedia(Media):
    body = models.FileField("움짤", upload_to="worldcup/media/gif/%Y/%m/%d/%H")


class VideoMedia(Media):
    body = models.CharField("외부 동영상 링크", max_length=255)
