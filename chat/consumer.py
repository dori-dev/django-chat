"""chat consumer
"""
from typing import Union
import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data: Union[str, bytes]):
        text_data_dict: dict = json.loads(text_data)
        message: str = text_data_dict['message']
        self.send(text_data=json.dumps({
            'message': message*2
        }))
