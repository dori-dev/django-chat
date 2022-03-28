"""chat views
"""
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request: object):
    return render(request, "index.html")


def room(request: object, room_name: str):
    username = request.user.username
    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username)),
    }
    return render(request, "room.html", context)
