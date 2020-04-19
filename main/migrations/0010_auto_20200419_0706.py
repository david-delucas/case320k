# Generated by Django 3.0.5 on 2020-04-19 07:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200419_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesscase',
            name='bc_creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 19, 7, 6, 42, 28492, tzinfo=utc), verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='timeseries',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 19, 7, 6, 42, 354707, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='timeseries',
            name='department',
            field=models.CharField(default='Default Dept1', max_length=30),
        ),
    ]
