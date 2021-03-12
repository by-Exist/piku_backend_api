from django.db import models
from django.core.validators import MinLengthValidator
from accountapp.models.user import CustomUser
from accountapp.validators import CustomUnicodeNicknameValidator


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
