"""chat views
"""
from django.shortcuts import render


def index(request: object):
    return render(request, "chat/index.html")


def room(request: object, room_name: str):
    context = {
        "room_name": room_name
    }
    return render(request, "chat/room.html", context)
