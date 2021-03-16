from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models, transaction
from . import models as accountapp_models
from .validators import (
    CustomASCIIUsernameValidator,
    CustomUnicodeNicknameValidator,
)


# TODO: 추후 auth를 잘 다룰 수 있게 되면, Group과 Permission에 대한 엔드포인트도 다루어야 할 지도 모르겠다.


class CustomUserManager(UserManager):
    @transaction.atomic
    def create_user_with_profile(
        self,
        user_kwargs,
        profile_kwargs,
    ):
        user_kwargs |= {
            "email": None,
            "is_staff": False,
            "is_superuser": False,
        }
        user = self._create_user(**user_kwargs)
        accountapp_models.Profile.objects.create(user=user, **profile_kwargs)
        return user


class CustomUser(AbstractUser):

    username = models.CharField(
        "ID",
        unique=True,
        max_length=20,
        error_messages={"max_length": "최대 15글자 까지 입력할 수 있습니다."},
        validators=[
            CustomASCIIUsernameValidator(),
            MinLengthValidator(8, "최소 5글자 이상 입력해주세요."),
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

    objects = CustomUserManager()


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
    email = models.EmailField("이메일", unique=True)
