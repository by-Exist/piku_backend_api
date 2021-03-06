# Generated by Django 3.1.6 on 2021-03-27 06:33

from django.db import migrations, models
import django.db.models.deletion
import worldcupapp.models.comment


class Migration(migrations.Migration):

    dependencies = [
        ("worldcupapp", "0018_auto_20210327_0525"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anonusercomment",
            name="comment_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="worldcupapp.comment",
            ),
        ),
        migrations.AlterField(
            model_name="authusercomment",
            name="comment_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="worldcupapp.comment",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="media",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=worldcupapp.models.comment.NON_POLYMORPHIC_CASCADE,
                to="worldcupapp.media",
                verbose_name="미디어",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="worldcup",
            field=models.ForeignKey(
                on_delete=worldcupapp.models.comment.NON_POLYMORPHIC_CASCADE,
                to="worldcupapp.worldcup",
                verbose_name="월드컵",
            ),
        ),
    ]
