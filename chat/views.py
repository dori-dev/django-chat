"""chat views
"""
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import json
from .models import Chat


def index(request: object):
    user = request.user
    context = {
        'best_groups': Chat.best_group(),
        'last_groups': Chat.last_group(),
    }
    if user.is_authenticated:
        your_groups = Chat.your_group(user)
        context['your_groups'] = your_groups
        context['your_groups_len'] = len(your_groups)
    return render(request, "chat/index.html", context)


@login_required(login_url="auth:register")
def room(request: object, room_name: str):
    room_name = slugify(room_name, allow_unicode=True)
    user = request.user
    chat_model = Chat.objects.filter(name=room_name)
    if chat_model.exists():
        chat_model[0].members.add(user)
    else:
        chat = Chat.objects.create(name=room_name)
        chat.members.add(user)
    chat = Chat.objects.get(name=room_name)
    room_id = chat.room_id
    return redirect(f'/id/{room_id}')


def group_list(request: object):
    user = request.user
    context = {
        'best_groups': Chat.best_group(),
        'last_groups': Chat.last_group(),
    }
    if user.is_authenticated:
        your_groups = Chat.your_group(user)
        context["your_groups"] = your_groups
        context["your_groups_len"] = len(your_groups)
    return render(request, "chat/group-list.html", context)


def create_group(request: object):
    return render(request, "chat/create-group.html")


@login_required(login_url="auth:register")
def group_view(request: object, room_id: str):
    username = request.user.username
    context = {
        "room_id": room_id,
        "username": mark_safe(json.dumps(username)),
        "name": request.user,
    }
    return render(request, "chat/room.html", context)
