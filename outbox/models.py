from random import uniform
import uuid
from django.db import models
from jsonfield.fields import JSONField
from django.utils import timezone
from datetime import timedelta


class Outbox(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    message_source = models.CharField(max_length=50)
    message_type = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True)
    next_attempt = models.DateTimeField(default=timezone.now)
    try_count = models.IntegerField(default=0)
    payload = JSONField()

    def ack(self):
        self.delivered_at = timezone.now()
        self.save(update_fields=['delivered_at'])

    def set_try(self):
        self.try_count += 1
        self.next_attempt += timedelta(
            seconds=uniform(0.5, 1) * 5 ** self.try_count
        )
        self.save()
