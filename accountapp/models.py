from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.urls import reverse
from accountapp.validators import (
    CustomASCIIUsernameValidator,
    CustomUnicodeNicknameValidator,
)


class CustomUser(AbstractUser):

    username = models.CharField(
        "ID",
        unique=True,
        max_length=20,
        error_messages={"max_length": "최대 15글자 까지 입력할 수 있습니다."},
        validators=[
            CustomASCIIUsernameValidator(),
            MinLengthValidator(5, "최소 5글자 이상 입력해주세요."),
        ],
    )
    password = models.CharField(
        "PW",
        max_length=128,
        validators=[
            MinLengthValidator(8, "최소 8글자 이상 입력해주세요."),
            MaxLengthValidator(20, "최대 20글자 까지 입력할 수 있습니다."),
        ],
    )

    def get_absolute_url(self):
        return reverse("account-detail", args=[self.id])


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(
        "닉네임",
        unique=True,
        max_length=13,
        validators=[
            MinLengthValidator(3, "세 글자 이상 입력해주세요."),
            CustomUnicodeNicknameValidator(),
        ],
    )
    avatar = models.ImageField(
        "아바타 이미지", blank=True, upload_to="accountapp/profile/%Y/%m/%d/%H"
    )
    email = models.EmailField("이메일")
