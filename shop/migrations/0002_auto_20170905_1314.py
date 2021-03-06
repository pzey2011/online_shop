# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='static/images/avatar.jpg', upload_to='static/images'),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='comment',
            field=models.TextField(max_length=500),
        ),
    ]
