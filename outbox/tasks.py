from celery import shared_task
from .models import Outbox
from .service import get_outbox_service
from django.db import transaction
from django.utils.timezone import now
from logging import getLogger
logger = getLogger(__name__)


@shared_task
def async_send_http_message(outbox_uuid):
    """
    Async jump for sending HTTP...
    """
    message = Outbox.objects.get(uuid=outbox_uuid)
    transport = get_outbox_service().get_transport(message.message_type)
    transport.do_post(message)


@shared_task
def resend_unsent_messages():
    with transaction.atomic():
        messages = Outbox.objects.filter(
            next_attempt__lte=now(),
            delivered_at__isnull=True,
        ).exclude(try_count__gte=10).order_by(
            'next_attempt'
        ).select_for_update()[0:100]
        outbox_service = get_outbox_service()
        for message in messages:
            outbox_service.send(message)
