"""chat views
"""
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json
from .models import Chat


def index(request: object):
    user = request.user
    context = {}
    if user.is_authenticated:
        chats: QuerySet[Chat] = Chat.objects.filter(
            members__username=user).order_by('-timestamp')
        chat_names = list(
            map(lambda chat: chat.name, chats)
        )
        context = {
            'chat_rooms': chat_names,
            'chat_rooms_length': len(chat_names),
        }
    return render(request, "chat/index.html", context)


@login_required(login_url="auth:register")
def room(request: object, room_name: str):
    # TODO
    user = request.user
    chat_model = Chat.objects.filter(name=room_name)
    if chat_model.exists():
        chat_model[0].members.add(user)
    else:
        chat = Chat.objects.create(name=room_name)
        chat.members.add(user)
    username = request.user.username
    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username)),
    }
    return render(request, "chat/room.html", context)


def group_list(request: object):
    return render(request, "chat/group-list.html")


def create_group(request: object):
    return render(request, "chat/create-group.html")
