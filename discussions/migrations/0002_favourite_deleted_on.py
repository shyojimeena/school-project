# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-06 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favourite',
            name='deleted_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
