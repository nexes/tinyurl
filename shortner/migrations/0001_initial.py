# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-02 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_name', models.TextField()),
                ('url_hash', models.CharField(max_length=80, unique=True)),
                ('usage_count', models.IntegerField(default=0)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
            ],
        ),
    ]