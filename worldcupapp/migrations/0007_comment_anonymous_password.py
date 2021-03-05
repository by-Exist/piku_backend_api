# Generated by Django 3.1.6 on 2021-03-05 06:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("worldcupapp", "0006_comment_anonymous_nickname"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="anonymous_password",
            field=models.CharField(
                default="",
                max_length=15,
                validators=[
                    django.core.validators.MinLengthValidator(
                        3, "세 글자 이상의 패스워드를 입력해주세요."
                    )
                ],
                verbose_name="익명 패스워드",
            ),
        ),
    ]
