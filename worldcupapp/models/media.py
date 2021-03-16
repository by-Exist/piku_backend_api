# # 테이블을 만드는 용도로 사용되며, 직접적으로 활용되지는 않음
# class BaseMedia(models.Model):
#     worldcup = models.ForeignKey(
#         Worldcup, on_delete=models.CASCADE, verbose_name="월드컵", related_name="media_set"
#     )
#     title = models.CharField("제목", max_length=31)
#     body = models.CharField("미디어", max_length=511)
#     win_count = models.PositiveIntegerField(
#         "승리 횟수", blank=True, default=0, editable=False
#     )
#     choice_count = models.PositiveIntegerField(
#         "1:1 선택 횟수", blank=True, default=0, editable=False
#     )

#     def get_absolute_url(self):
#         return reverse("media-detail", args=[self.worldcup.pk, self.id])

#     class Meta:
#         db_table = "Medias"


# class AbstractMedia(models.Model):
#     worldcup = models.ForeignKey(Worldcup, on_delete=models.CASCADE, verbose_name="월드컵")
#     title = models.CharField("제목", max_length=31)
#     win_count = models.PositiveIntegerField(
#         "승리 횟수", blank=True, default=0, editable=False
#     )
#     choice_count = models.PositiveIntegerField(
#         "1:1 선택 횟수", blank=True, default=0, editable=False
#     )

#     class Meta:
#         abstract = True


# class TextMedia(AbstractMedia):
#     body = models.CharField("Text 미디어", max_length=511)

#     class Meta:
#         db_table = "Medias"
#         managed = False


# class ImageMedia(AbstractMedia):
#     body = models.ImageField(
#         "Image 미디어", upload_to="worldcupapp/imagemedia/%Y/%m/%d/%H"
#     )

#     class Meta:
#         db_table = "Medias"
#         managed = False


# class GifMedia(AbstractMedia):
#     body = models.ImageField("Gif 미디어", upload_to="worldcupapp/gifmedia/%Y/%m/%d/%H")

#     class Meta:
#         db_table = "Medias"
#         managed = False


# class VideoMedia(AbstractMedia):
#     body = models.CharField("Video 미디어", max_length=255)

#     class Meta:
#         db_table = "Medias"
#         managed = False
