# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-18 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontauth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='frontusermodel',
            old_name='joined_date',
            new_name='date_joined',
        ),
    ]
