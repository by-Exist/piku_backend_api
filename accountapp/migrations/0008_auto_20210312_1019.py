# Generated by Django 3.1.6 on 2021-03-12 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accountapp", "0007_auto_20210312_0716"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="email",
        ),
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="이메일"),
        ),
    ]
