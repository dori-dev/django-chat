"""chat consumer
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name: str = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name)

    async def receive(self, text_data: str):
        """receive data from WebSocket

        Args:
            text_data (str): text data
        """
        text_data_dict: dict = json.loads(text_data)
        message: str = text_data_dict['message']
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event: dict):
        """receive message from room group

        Args:
            event (dict): the event
        """
        message: str = event['message']
        # send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
