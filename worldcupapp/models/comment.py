from copy import deepcopy
from django.db import models
from django.contrib.auth import get_user_model
from polymorphic.models import PolymorphicModel
from accountapp.models import Profile
from ..models import Worldcup, Media


# polymorphic 모델의 계단식 삭제가 올바르게 적용되지 않는 문제 해결
# https://github.com/django-polymorphic/django-polymorphic/issues/229
def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class Comment(PolymorphicModel):

    worldcup = models.ForeignKey(
        Worldcup, on_delete=NON_POLYMORPHIC_CASCADE, verbose_name="월드컵"
    )
    media = models.ForeignKey(
        Media,
        null=True,
        blank=True,
        on_delete=NON_POLYMORPHIC_CASCADE,
        verbose_name="미디어",
    )
    body = models.CharField("댓글 내용", max_length=511)
    created_at = models.DateTimeField("작성시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정시각", auto_now=True)


class AuthUserComment(Comment):

    writer = models.ForeignKey(
        get_user_model(), blank=True, on_delete=models.CASCADE, verbose_name="작성자"
    )


class AnonUserComment(Comment):

    anon_nickname = models.CharField(
        "익명 닉네임",
        max_length=Profile()._meta.get_field("nickname").max_length,
        validators=deepcopy(Profile()._meta.get_field("nickname").validators),
    )
    anon_password = models.CharField(
        "익명 패스워드",
        max_length=get_user_model()()._meta.get_field("password").max_length,
        validators=deepcopy(get_user_model()()._meta.get_field("password").validators),
    )
