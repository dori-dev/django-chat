"""chat views
"""
from django.shortcuts import render


def index(request: object):
    return render(request, "chat/index.html")
