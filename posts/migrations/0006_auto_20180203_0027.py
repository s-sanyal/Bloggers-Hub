# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-02 18:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20180203_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 2, 2, 18, 57, 52, 374000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
