# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-20 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_keypair_pubkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='encrypt',
            field=models.BooleanField(default=False),
        ),
    ]
