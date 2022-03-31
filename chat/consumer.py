"""chat consumer
"""
from django.db.models.query import QuerySet
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from .serializers import MessageSerializer
from .models import Chat, Message, User


class ChatConsumer(WebsocketConsumer):
    """chat consumer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands: dict = {
            "new_message": "message",
            "send_image": "image",
            "message": "new_message",
            "image": "send_image",
        }

    def new_message(self, data: dict):
        author = User.objects.get(username=data['username'])
        room = Chat.objects.get(room_id=data['room_name'])
        type = self.commands[data['command']]
        # use `objects.create` because I just want `insert` message!
        Message.objects.create(
            author=author,
            content=data['message'],
            room=room,
            type=type)

    def fetch_message(self, room_name: str):
        query_set: QuerySet[Message] = Message.last_messages(room_name)
        content: bytes = self.message_serializer(query_set)
        messages: list = reversed(json.loads(content))
        for message in messages:
            self.chat_message(
                {
                    "message": message['content'],
                    "author": message['author_username'],
                    "command": self.commands[message['type']]
                }
            )

    def send_image(self, data: dict):
        self.new_message(data)
        self.send_to_room(data)

    def message_serializer(self, query_set: QuerySet[Message]):
        serialized: list = MessageSerializer(query_set, many=True)
        content: bytes = JSONRenderer().render(serialized.data)
        return content

    def connect(self):
        self.room_id: str = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name)

    def receive(self, text_data: str):
        """receive data from WebSocket

        Args:
            text_data (str): text data
        """
        data_dict: dict = json.loads(text_data)
        command: str = data_dict['command']
        # execute the function according to the given `command`
        if command == 'new_message':
            message: str = data_dict['message']
            if not message.strip():
                return
            self.new_message(data_dict)
            self.send_to_room(data_dict)
        elif command == 'fetch_message':
            room_name: str = data_dict['room_name']
            self.fetch_message(room_name)
        elif command == 'send_image':
            self.send_image(data_dict)
        else:
            print(f'Invalid Command: "{command}"')

    def send_to_room(self, data: dict):
        """send message to room group

        Args:
            message (str): message will send
        """
        message: str = data['message']
        author: str = data['username']
        command: str = data.get("command", "new_message")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': author,
                'command': command,
            }
        )

    def chat_message(self, event: dict):
        """receive message from room group

        Args:
            event (dict): the event
        """
        # send message to WebSocket
        self.send(text_data=json.dumps(event))
