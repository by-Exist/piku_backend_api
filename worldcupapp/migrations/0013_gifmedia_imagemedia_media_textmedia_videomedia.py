# Generated by Django 3.1.6 on 2021-03-17 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("worldcupapp", "0012_worldcup_view_count"),
    ]

    operations = [
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=31, verbose_name="제목")),
                (
                    "win_count",
                    models.PositiveIntegerField(
                        blank=True, default=0, editable=False, verbose_name="승리 횟수"
                    ),
                ),
                (
                    "view_count",
                    models.PositiveBigIntegerField(
                        blank=True, default=0, editable=False, verbose_name="등장 횟수"
                    ),
                ),
                (
                    "choice_count",
                    models.PositiveIntegerField(
                        blank=True, default=0, editable=False, verbose_name="선택 횟수"
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_worldcupapp.media_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "worldcup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media_set",
                        to="worldcupapp.worldcup",
                        verbose_name="월드컵",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="GifMedia",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="worldcupapp.media",
                    ),
                ),
                (
                    "body",
                    models.FileField(
                        upload_to="worldcup/media/gif/%Y/%m/%d/%H", verbose_name="움짤"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("worldcupapp.media",),
        ),
        migrations.CreateModel(
            name="ImageMedia",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="worldcupapp.media",
                    ),
                ),
                (
                    "body",
                    models.ImageField(
                        upload_to="worldcup/media/image/%Y/%m/%d/%H", verbose_name="이미지"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("worldcupapp.media",),
        ),
        migrations.CreateModel(
            name="TextMedia",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="worldcupapp.media",
                    ),
                ),
                ("body", models.TextField(max_length=1023, verbose_name="텍스트")),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("worldcupapp.media",),
        ),
        migrations.CreateModel(
            name="VideoMedia",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="worldcupapp.media",
                    ),
                ),
                ("body", models.CharField(max_length=255, verbose_name="외부 동영상 링크")),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("worldcupapp.media",),
        ),
    ]
