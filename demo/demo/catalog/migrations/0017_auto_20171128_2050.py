# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-29 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(upload_to='demo/catalog/images/'),
        ),
    ]