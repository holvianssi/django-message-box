from celery import shared_task
from .models import Outbox
from .service import get_outbox_service
from django.db import DatabaseError
from django.db import transaction
from django.utils.timezone import now
from logging import getLogger
logger = getLogger(__name__)


@shared_task
def async_send(outbox_uuid):
    """
    Send the message. In case the message has been already delivered
    or if there's another process handling it (nowait=True select_for_update
    raise DatabaseError) skip the processing, as the message is or
    will be processed by another process.
    """
    with transaction.atomic():
        try:
            message = Outbox.objects.select_for_update(nowait=True).get(
                uuid=outbox_uuid
            )
            if message.delivered_at:
                return
        except DatabaseError:
            return
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
