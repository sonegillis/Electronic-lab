# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-14 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20180714_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentborrowtransactions',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
