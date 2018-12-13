from django.db import connection
from .models import Outbox
from logging import getLogger
logger = getLogger('__name__')


class OutboxService(object):
    def __init__(self):
        self.config = {}

    def configure(self, message_type, transport):
        self.config[message_type] = transport

    def create_message(self, message_source, message_type, payload):
        message = Outbox.objects.create(
            message_source=message_source, message_type=message_type,
            payload=payload)
        connection.on_commit(lambda: self.send(message))

    def send(self, message, force=False):
        if not force:
            if message.delivered_at:
                raise Exception("This message has been already delivered")
        transport = self.get_transport(message.message_type)
        message.set_try()
        try:
            transport.send(message)
        except:
            logger.exception(
                "Error in transport.send() for message %s",
                message.uuid)

    def get_transport(self, message_type):
        return self.config[message_type]


_service = OutboxService()


def get_outbox_service():
    # Mock me, and you'll get whatever you want for the service.
    return _service
