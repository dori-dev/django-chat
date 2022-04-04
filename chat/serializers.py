from datetime import datetime
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['author_username', 'content', 'type', 'time']

    def get_time(self, message: Message):
        time = datetime.strftime(
            message.timestamp.astimezone(),
            "%I:%M %p")
        return time
