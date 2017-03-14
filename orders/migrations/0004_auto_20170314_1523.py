# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-14 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import orders.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20170314_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickup_date',
            field=models.DateField(validators=[orders.models.after_yesterday, orders.models.is_during_the_season]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True),
        ),
    ]