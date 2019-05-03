# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-05-01 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide_image',
            name='url',
            field=models.ImageField(upload_to='', verbose_name='轮播图图片url'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(upload_to='', verbose_name='用户头像路径'),
        ),
    ]