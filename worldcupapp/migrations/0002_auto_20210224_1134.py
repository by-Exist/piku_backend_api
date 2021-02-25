# Generated by Django 3.1.6 on 2021-02-24 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("worldcupapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basemedia",
            name="choice_count",
            field=models.PositiveIntegerField(
                blank=True, default=0, editable=False, verbose_name="1:1 선택 횟수"
            ),
        ),
        migrations.AlterField(
            model_name="basemedia",
            name="win_count",
            field=models.PositiveIntegerField(
                blank=True, default=0, editable=False, verbose_name="승리 횟수"
            ),
        ),
        migrations.AlterField(
            model_name="worldcup",
            name="play_count",
            field=models.PositiveIntegerField(
                blank=True, default=0, editable=False, verbose_name="플레이 완료 횟수"
            ),
        ),
        migrations.AlterField(
            model_name="worldcup",
            name="title",
            field=models.CharField(
                max_length=63,
                validators=[
                    django.core.validators.MinLengthValidator(3, "세 글자 이상 입력해주세요.")
                ],
                verbose_name="제목",
            ),
        ),
    ]
