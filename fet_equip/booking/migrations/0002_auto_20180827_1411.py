# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-27 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('phoneNumber', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StaffBookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(max_length=10)),
                ('reason', models.CharField(choices=[('Work', 'work'), ('Class', 'class')], max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='StudentBookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(max_length=20)),
                ('Matricule', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='WeekDaySchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekDay', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('fromTime', models.TimeField()),
                ('toTime', models.TimeField()),
                ('maxBookings', models.IntegerField(default=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Friday',
        ),
        migrations.DeleteModel(
            name='Monday',
        ),
        migrations.DeleteModel(
            name='Saturday',
        ),
        migrations.DeleteModel(
            name='Sunday',
        ),
        migrations.DeleteModel(
            name='Thursday',
        ),
        migrations.DeleteModel(
            name='Tuesday',
        ),
        migrations.DeleteModel(
            name='Wednesday',
        ),
        migrations.AddField(
            model_name='studentbookings',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.WeekDaySchedule'),
        ),
        migrations.AddField(
            model_name='staffbookings',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.WeekDaySchedule'),
        ),
    ]
