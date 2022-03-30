"""chat views
"""
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json
from .models import Message
from .models import Chat  # TODO


def index(request: object):
    user = request.user
    context = {}
    if user.is_authenticated:
        messages: QuerySet[Message] = Message.objects.filter(
            author__username=user)  # TODO sort by last message in top
        chat_rooms = set(
            map(lambda message: message.room_name, messages)
        )
        context = {
            'chat_rooms': chat_rooms,
            'chat_rooms_length': len(chat_rooms),
        }
    return render(request, "chat/index.html", context)


@login_required(login_url="auth:register")
def room(request: object, room_name: str):
    # TODO
    user = request.user
    chat_model = Chat.objects.filter(room_name=room_name)
    if chat_model.exists():
        chat_model[0].members.add()
    else:
        chat = Chat.objects.create(room_name=room_name)
        chat.members.add(user)
    username = request.user.username
    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username)),
    }
    return render(request, "chat/room.html", context)
