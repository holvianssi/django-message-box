# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Outbox',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('message_source', models.CharField(max_length=50)),
                ('message_type', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('delivered_at', models.DateTimeField(null=True)),
                ('next_attempt', models.DateTimeField(default=timezone.now)),
                ('try_count', models.IntegerField(default=0)),
                ('payload', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
    ]
