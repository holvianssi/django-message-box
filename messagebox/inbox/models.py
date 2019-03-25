from django.db import models
try:
    from django.contrib.postgres.fields import JSONField
except ImportError:
    from jsonfield.fields import JSONField


class Inbox(models.Model):
    uuid = models.UUIDField(primary_key=True)
    message_source = models.CharField(max_length=50)
    message_type = models.CharField(max_length=50)
    origin_create_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    payload = JSONField()
