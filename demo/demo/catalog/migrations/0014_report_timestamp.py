# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_report_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
