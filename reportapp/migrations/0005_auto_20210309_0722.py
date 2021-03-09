# Generated by Django 3.1.6 on 2021-03-09 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reportapp", "0004_auto_20210304_0613"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commentreport",
            name="reason",
            field=models.CharField(
                choices=[
                    ("Sex", "성적 요소가 포함되어 있습니다."),
                    ("Hate", "증오/혐오 등의 내용이 포함되어 있습니다."),
                    ("Spam", "스팸 및 광고성 내용이 포함되어 있습니다."),
                    ("Child", "아동학대 관련 내용이 포함되어 있습니다."),
                    ("Other", "기타"),
                ],
                max_length=15,
                verbose_name="신고 사유",
            ),
        ),
        migrations.AlterField(
            model_name="mediareport",
            name="reason",
            field=models.CharField(
                choices=[
                    ("Sex", "성적 요소가 포함되어 있습니다."),
                    ("Hate", "증오/혐오 등의 내용이 포함되어 있습니다."),
                    ("Spam", "스팸 및 광고성 내용이 포함되어 있습니다."),
                    ("Child", "아동학대 관련 내용이 포함되어 있습니다."),
                    ("Other", "기타"),
                ],
                max_length=15,
                verbose_name="신고 사유",
            ),
        ),
        migrations.AlterField(
            model_name="userreport",
            name="reason",
            field=models.CharField(
                choices=[
                    ("Sex", "성적 요소가 포함되어 있습니다."),
                    ("Hate", "증오/혐오 등의 내용이 포함되어 있습니다."),
                    ("Spam", "스팸 및 광고성 내용이 포함되어 있습니다."),
                    ("Child", "아동학대 관련 내용이 포함되어 있습니다."),
                    ("Other", "기타"),
                ],
                max_length=15,
                verbose_name="신고 사유",
            ),
        ),
        migrations.AlterField(
            model_name="worldcupreport",
            name="reason",
            field=models.CharField(
                choices=[
                    ("Sex", "성적 요소가 포함되어 있습니다."),
                    ("Hate", "증오/혐오 등의 내용이 포함되어 있습니다."),
                    ("Spam", "스팸 및 광고성 내용이 포함되어 있습니다."),
                    ("Child", "아동학대 관련 내용이 포함되어 있습니다."),
                    ("Other", "기타"),
                ],
                max_length=15,
                verbose_name="신고 사유",
            ),
        ),
    ]
