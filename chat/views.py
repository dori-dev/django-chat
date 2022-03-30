"""chat views
"""
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
# from django.utils.text import slugify  # TODO
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
    # print(f"<{slugify(room_name, allow_unicode=False)}>")  # TODO
    # room_name = slugify(room_name, allow_unicode=False).replace("-", "")
    # room_name == slugfy_name  TODO use id for room
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
        "name": request.user,
    }
    return render(request, "chat/room.html", context)


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
