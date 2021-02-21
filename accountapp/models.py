from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(
        "닉네임", unique=True, max_length=13, validators=[MinLengthValidator(3)]
    )
    avatar = models.ImageField(
        "아바타 이미지", blank=True, upload_to="accountapp/profile/%Y/%m/%d/%H"
    )
    email = models.EmailField("이메일", blank=True)
