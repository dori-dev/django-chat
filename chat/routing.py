"""chat routing
"""
from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/id/(?P<room_id>\w+)/$', consumer.ChatConsumer.as_asgi()),
]
