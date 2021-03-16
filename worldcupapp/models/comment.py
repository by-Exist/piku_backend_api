# class Comment(models.Model):
#     writer = models.ForeignKey(
#         get_user_model(),
#         null=True,
#         blank=True,
#         on_delete=models.CASCADE,
#         verbose_name="작성자",
#     )
#     anonymous_nickname = models.CharField(
#         "익명 닉네임",
#         default="익명",
#         max_length=13,
#     )
#     anonymous_password = models.CharField(
#         "익명 패스워드",
#         max_length=15,
#     )
#     worldcup = models.ForeignKey(Worldcup, on_delete=models.CASCADE, verbose_name="월드컵")
#     media = models.ForeignKey(
#         BaseMedia, null=True, blank=True, on_delete=models.CASCADE, verbose_name="미디어"
#     )
#     comment = models.CharField("댓글 내용", max_length=511)
#     created_at = models.DateTimeField("작성시각", auto_now_add=True)
#     updated_at = models.DateTimeField("수정시각", auto_now=True)

#     def get_absolute_url(self):
#         return reverse("comment-detail", args=[self.worldcup.pk, self.id])
