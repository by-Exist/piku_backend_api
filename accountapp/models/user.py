from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from accountapp import models as accountapp_models
from accountapp.validators import CustomASCIIUsernameValidator


class CustomUserManager(UserManager):
    def create_user_with_profile(
        self,
        username,
        password,
        profile_nickname,
        profile_email,
        user_kwargs,
        profile_kwargs,
    ):
        user_kwargs.setdefault("is_staff", False)
        user_kwargs.setdefault("is_superuser", False)
        user = self._create_user(
            username=username, email=None, password=password, **user_kwargs
        )
        accountapp_models.Profile.objects.create(
            user=user, nickname=profile_nickname, email=profile_email, **profile_kwargs
        )
        return user


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

    objects = CustomUserManager()