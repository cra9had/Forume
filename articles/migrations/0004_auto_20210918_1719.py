# Generated by Django 3.2.7 on 2021-09-18 17:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20210918_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='PublicDate',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 18, 17, 19, 3, 398049, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='article',
            name='ShortText',
            field=models.CharField(max_length=140),
        ),
    ]
