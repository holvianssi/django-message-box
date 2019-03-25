from datetime import timedelta
from django.utils import timezone
from random import uniform
import requests

from logging import getLogger
logger = getLogger(__name__)


class BaseTransport(object):
    MAX_RETRIES = 10

    def send(self, message):
        raise NotImplementedError

    def set_next_try(self, message):
        # Exponential backoff with at least 15 seconds between
        # attempts.
        message.try_count += 1
        message.next_attempt = max(
            message.next_attempt + timedelta(
                seconds=uniform(0.5, 1) * 5 ** message.try_count
            ),
            timezone.now() + timedelta(seconds=uniform(15, 60))
        )

    def on_failure(self, message):
        if message.try_count < self.MAX_RETRIES:
            self.set_next_try(message)
        else:
            message.next_attempt = None
            logger.error("Permanent failure for message %s", message.uuid)
        message.save(update_fields=['next_attempt', 'try_count'])

    def get_payload(self, message):
        return {
            'uuid': str(message.uuid),
            'message_source': message.message_source,
            'message_type': message.message_type,
            'origin_create_time': message.create_time.isoformat(),
            'payload': message.payload
        }


class HttpTransport(BaseTransport):
    def __init__(self, to):
        self.to = to

    def send(self, message):
        """
        Handles sending the message.
        """
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
