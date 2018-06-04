# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-31 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_auto_20180302_0029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogs',
            options={'ordering': ['-views']},
        ),
        migrations.AlterField(
            model_name='blogs',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Profile'),
        ),
        migrations.AlterField(
            model_name='blogs',
            name='title',
            field=models.CharField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='genre',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
