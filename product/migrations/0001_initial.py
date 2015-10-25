# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sku', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('model', models.CharField(max_length=100)),
                ('length', models.FloatField(null=True, blank=True)),
                ('breadth', models.FloatField(null=True, blank=True)),
                ('height', models.FloatField(null=True, blank=True)),
                ('image', models.ImageField(upload_to='images')),
                ('thumbnail', models.ImageField(null=True, blank=True, upload_to='images')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
