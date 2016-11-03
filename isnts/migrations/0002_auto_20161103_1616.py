# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isnts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blood_type',
            name='RH',
            field=models.BooleanField(choices=[(True, '+'), (False, '-')]),
        ),
        migrations.AlterField(
            model_name='blood_type',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'B'), (2, 'AB'), (3, '0'), (0, 'A')]),
        ),
    ]
