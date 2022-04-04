"""chat views
"""
from django.core.paginator import Paginator
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
    if room_name == "listener":
        return redirect("/chat/listener2")
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
    all_groups = Chat.all_groups()
    paginator = Paginator(all_groups, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, "chat/group-list.html", context)


def create_group(request: object):
    return render(request, "chat/create-group.html")


@login_required(login_url="auth:register")
def group_view(request: object, room_id: str):
    if room_id == "BFoULH5Z":
        return redirect("/chat/listener2")
    user = request.user
    chat_model = Chat.objects.filter(room_id=room_id)
    if chat_model.exists():
        chat_model[0].members.add(user)
    else:
        return redirect("index")
    username = request.user.username
    context = {
        "room_id": room_id,
        "username": mark_safe(json.dumps(username)),
        "name": user,
        "room": chat_model[0].name,
    }
    return render(request, "chat/room.html", context)


def about(request: object):
    return render(request, "chat/about.html")
