# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-20 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0026_profile_cover_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='topic_logo',
            field=models.FileField(default='default.png', upload_to=b''),
        ),
    ]