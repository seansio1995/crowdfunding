# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-29 01:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_message_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='', upload_to='images/'),
            preserve_default=False,
        ),
    ]
