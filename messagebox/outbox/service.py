from django.db import connection
from django.utils import timezone
from datetime import timedelta
from .models import Outbox
from logging import getLogger
logger = getLogger(__name__)


class OutboxService(object):
    def __init__(self):
        self.config = {}

    def register_transport(self, message_source, message_type, transport):
        self.config[(message_source, message_type)] = transport

    def create_message(self, message_source, message_type, payload,
                       delay=0):
        from messagebox.outbox.tasks import async_send
        message = Outbox.objects.create(
            message_source=message_source, message_type=message_type,
            payload=payload,
            next_attempt=timezone.now() + timedelta(seconds=delay))
        if delay == 0:
            connection.on_commit(
                lambda: async_send.delay(outbox_uuid=message.uuid))

    def send(self, message, force=False):
        if not force and message.delivered_at:
            raise Exception("This message has been already delivered")
        transport = self.get_transport(
            message.message_source, message.message_type)
        try:
            transport.send(message)
        except Exception:
            logger.exception(
                "Error in transport.send() for message %s",
                message.uuid)
        if message.delivered_at is None:
            transport.on_failure(message)

    def get_transport(self, message_source, message_type):
        return self.config[(message_source, message_type)]


_service = OutboxService()


def get_outbox_service():
    # Mock me, and you'll get whatever you want for the service.
    return _service
