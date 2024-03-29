# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-30 23:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.AlterField(
            model_name='report',
            name='files',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.file'),
        ),
    ]
