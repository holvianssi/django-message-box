import uuid
from django.db import models
from jsonfield.fields import JSONField
from django.utils import timezone


class Outbox(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    message_source = models.CharField(max_length=50)
    message_type = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True)
    next_attempt = models.DateTimeField(default=timezone.now, db_index=True,
                                        null=True)
    try_count = models.IntegerField(default=0)
    payload = JSONField()

    def ack(self):
        self.delivered_at = timezone.now()
        self.next_attempt = None
        self.save(update_fields=['delivered_at', 'next_attempt'])
