# Generated by Django 3.1.6 on 2021-03-23 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        ("worldcupapp", "0016_auto_20210322_0750"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
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
                (
                    "body",
                    models.CharField(blank=True, max_length=511, verbose_name="신고 내용"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="reportapp/report/%Y/%m/%d",
                        verbose_name="증빙 사진",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="작성일"),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_reportapp.report_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="신고자",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="WorldcupReport",
            fields=[
                (
                    "report_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reportapp.report",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        choices=[("WORLDCUPEXAMPLE", "월드컵 신고 사유 예제")],
                        max_length=15,
                        verbose_name="신고 사유",
                    ),
                ),
                (
                    "reported",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="worldcupapp.worldcup",
                        verbose_name="신고된 월드컵",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("reportapp.report",),
        ),
        migrations.CreateModel(
            name="UserReport",
            fields=[
                (
                    "report_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reportapp.report",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        choices=[("USEREXAMPLE", "유저 신고 사유 예제")],
                        max_length=15,
                        verbose_name="신고 사유",
                    ),
                ),
                (
                    "reported",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="신고된 유저",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("reportapp.report",),
        ),
        migrations.CreateModel(
            name="MediaReport",
            fields=[
                (
                    "report_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reportapp.report",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        choices=[("MEDIAEXAMPLE", "미디어 신고 사유 예제")],
                        max_length=15,
                        verbose_name="신고 사유",
                    ),
                ),
                (
                    "reported",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="worldcupapp.media",
                        verbose_name="신고된 미디어",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("reportapp.report",),
        ),
        migrations.CreateModel(
            name="CommentReport",
            fields=[
                (
                    "report_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="reportapp.report",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        choices=[("COMMENTEXAMPLE", "댓글 신고 사유 예제")],
                        max_length=15,
                        verbose_name="신고 사유",
                    ),
                ),
                (
                    "reported",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="worldcupapp.comment",
                        verbose_name="신고된 댓글",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("reportapp.report",),
        ),
    ]
