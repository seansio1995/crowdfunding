# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-02 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_auto_20171202_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='average_rate',
            field=models.FloatField(default=0),
        ),
    ]
