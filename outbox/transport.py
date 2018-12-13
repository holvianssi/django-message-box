from .tasks import async_send_http_message
import requests

from logging import getLogger
logger = getLogger(__name__)


class BaseTransport(object):
    def send(self, message):
        raise NotImplementedError


class HTTPTransport(object):
    def __init__(self, to, async=True, require_separate_ack=False):
        self.to = to
        self.async = async
        self.require_separate_ack = require_separate_ack

    def send(self, message):
        """
        Handles sending the message, asynchronously if the transport is
        so configured. In essense wrapper for do_post().

        If you want to customise how the POST is done, override do_post().
        """
        if self.async:
            async_send_http_message.delay(outbox_uuid=message.uuid)
        else:
            self.do_post(message)

    def do_post(self, message):
        headers = {'Content-type': 'application/json'}
        payload = self.get_payload(message)
        response = requests.post(
            self.to, json=payload, headers=headers)
        if response.status_code not in (200, 201):
            logger.error(
                "Got status_code %s for message %s (try count %d). "
                "Content was %s", response.status_code, message.uuid,
                message.try_count, response.content
            )
        else:
            message.ack()

    def get_payload(self, message):
        return {
            'uuid': str(message.uuid),
            'message_source': message.message_source,
            'message_type': message.message_type,
            'origin_create_time': message.create_time.isoformat(),
            'payload': message.payload
        }
