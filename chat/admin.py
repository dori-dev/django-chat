"""chat admin
"""
from datetime import datetime
from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "time", "room_name")
    list_filter = ("author", "room_name", "timestamp")

    def time(self, model: object):
        date: datetime = model.timestamp.astimezone()
        format_date = datetime.strftime(date, "%b %d, %H:%M:%S")
        return format_date


admin.site.register(Message, MessageAdmin)
