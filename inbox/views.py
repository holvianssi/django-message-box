from rest_framework import serializers
from rest_framework import generics
from .service import get_inbox_service
from .models import Inbox


try:
    class JSONField(serializers.WritableField):
        def to_native(self, obj):
            return obj
except AttributeError:
    from rest_framework.serializers import JSONField


class ReceiveMessageSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField()
    payload = JSONField()

    class Meta:
        model = Inbox
        fields = (
            'origin_create_time', 'uuid', 'message_source',
            'message_type', 'payload'
        )

    def create(self, validated_data):
        return get_inbox_service().handle_message(validated_data)


class ReceiveMessageView(generics.CreateAPIView):
    serializer_class = ReceiveMessageSerializer
