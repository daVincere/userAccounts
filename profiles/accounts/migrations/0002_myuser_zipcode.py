# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-09 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='zipcode',
            field=models.CharField(default=b'110010', max_length=120),
        ),
    ]
