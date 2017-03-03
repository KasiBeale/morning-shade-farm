# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-03 02:45
from __future__ import unicode_literals

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_date', models.DateField()),
                ('quantity', models.IntegerField(validators=[orders.models.multiple_of_ten, orders.models.greater_than_zero])),
                ('requester_name', models.CharField(max_length=128)),
                ('requester_email', models.CharField(max_length=128)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('FULFILLED', 'Fulfilled'), ('CANCELED', 'Canceled')], default='PENDING', max_length=128)),
            ],
        ),
    ]
