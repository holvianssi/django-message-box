from django.db import transaction


class InboxService(object):
    def __init__(self):
        self.handlers = {}

    def register_handler(self, message_source, message_type, handler):
        assert callable(handler)
        self.handlers[(message_source, message_type)] = handler

    def handle_message(self, data):
        from .models import Inbox
        with transaction.atomic():
            existing = Inbox.objects.filter(uuid=data['uuid']).first()
            if existing:
                return existing
            else:
                message = Inbox.objects.create(**data)
                handler = self.handlers.get(
                    (data['message_source'], data['message_type'])
                )
                handler(message)
                return message


_service = InboxService()


def get_inbox_service():
    # Mock me, and you'll get whatever you want for the service.
    return _service
