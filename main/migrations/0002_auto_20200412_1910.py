# Generated by Django 3.0.5 on 2020-04-12 19:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesscase',
            name='bc_creation_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 12, 19, 10, 40, 182332, tzinfo=utc), verbose_name='Creation date'),
        ),
    ]
