# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-07 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_modemstate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModemImeiNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtn_key_imei', models.CharField(max_length=100)),
                ('orange_key_imei', models.CharField(max_length=100)),
            ],
        ),
    ]
