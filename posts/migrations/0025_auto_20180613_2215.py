# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-13 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_auto_20180613_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.FileField(default='blank-profile-picture-973460_640.png', upload_to=b''),
        ),
    ]