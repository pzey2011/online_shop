# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 11:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('comment', models.CharField(max_length=500)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('status', models.CharField(choices=[('requested', 'requested'), ('canceled', 'canceled'), ('pending', 'pending'), ('finished', 'finished')], default='requested', max_length=1)),
                ('items', models.ManyToManyField(to='shop.Item')),
            ],
        ),
    ]
