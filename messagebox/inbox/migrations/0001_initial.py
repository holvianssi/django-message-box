# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
try:
    from django.contrib.postgres.fields import JSONField
except ImportError:
    from jsonfield.fields import JSONField

import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('message_source', models.CharField(max_length=50)),
                ('message_type', models.CharField(max_length=50)),
                ('origin_create_time', models.DateTimeField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('payload', JSONField(default=dict)),
            ],
        ),
    ]
