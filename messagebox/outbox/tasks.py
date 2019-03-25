from celery import shared_task
from .models import Outbox
from .service import get_outbox_service
from django.db import transaction
from django.utils.timezone import now
from logging import getLogger
logger = getLogger(__name__)


@shared_task
def async_send(outbox_uuid):
    """
    Async jump for sending HTTP...
    """
    with transaction.atomic():
        message = Outbox.objects.select_for_update().get(uuid=outbox_uuid)
        get_outbox_service().send(message)


@shared_task
def resend_unsent_messages():
    messages = Outbox.objects.filter(
        next_attempt__lte=now()
    ).order_by(
        'next_attempt'
    )[0:500]
    for message in messages:
        async_send.delay(message.uuid)
