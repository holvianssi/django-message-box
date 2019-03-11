# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('outbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outbox',
            name='next_attempt',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, db_index=True),
        ),
    ]
