# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 16:31
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=120)),
            ],
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=120, unique=True, validators=[django.core.validators.RegexValidator(code=b'invalid_username', message=b'Username must be alphanumeric or contain ".@+-"', regex=b'^[a-zA-Z0-9]*$')]),
        ),
        migrations.AddField(
            model_name='activationprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
