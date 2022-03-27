"""chat consumer
"""
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name: str = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.room_group_name = f'chat_{self.room_name}'
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
        text_data_dict: dict = json.loads(text_data)
        message: str = text_data_dict['message']
        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event: dict):
        """receive message from room group

        Args:
            event (dict): the event
        """
        message: str = event['message']
        # send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
